# The image tagging system of PyTFall:
init -9 python:
    class TagDatabase(_object):
        '''Maps image tags to image paths.
        
        sample entry of self.tagmap:
        tag : set([relative path to image 1, relative path to image 2, ...])  
        '''
        @classmethod
        def from_json(cls, filepaths=[]):
            '''Returns a new TagDatabase instance with data from JSON files.
            
            If filepaths is empty, an empty TagDatabase instance is returned.
            '''
            tdb = TagDatabase()
            
            if not filepaths:
                return tdb
            else:
                for entry in filepaths:
                    for fp in entry:
                        if len(fp.split("game%s" % os.sep)[1].split(os.sep)) == 4:
                            # deserialize JSON file into a python dict
                            with open(fp, "r") as f:
                                imgmap = json.load(f)
                            # add the images and their tags to the database
                            for imgpath in imgmap:
                                taglist = imgmap[imgpath]
                                tdb.add_image(imgpath, taglist)
                        else:     # New style tags from tagger software
                            # deserialize JSON file into a python dict
                            with open(fp, "r") as f:
                                imgmap = json.load(f)
                            # add the images and their tags to the database
                            # adjusting path and adding girl id to tags as required for tags to function in PyTFall
                            path = fp.split("game%s" % os.sep)[1][:-9]
                            for imgpath in imgmap[2]:
                                # ID
                                imgmap[2][imgpath].append(fp.split(os.sep)[-2])
                                taglist = imgmap[2][imgpath]
                                # Path
                                imgpath = "".join([path,  imgpath])
                                tdb.add_image(imgpath, taglist)
                return tdb
                
        def __init__(self):
            # maps image tags to sets of image paths
            self.all_tags = set(tags_dict.values())
            self.tagmap = {}
            # stores relative paths to untagged images
            self.untagged = set()
            
        # add images with or without tags to the database
        #-----------------------------------
            
        def add_image(self, relpath, tags=[]):
            '''Adds the image at relpath to the database.
            
            If tags is defined, it must be an iterable containing strings.
            If tags is not defined, the image will be added to the set of 
            untagged images.
            '''
            assert isinstance(relpath, basestring) or isinstance(relpath, unicode)
            if tags is []:
                self.untagged.add(relpath)
            else:
                for t in tags:
                    self.add_tag(t, relpath)
                    
        def add_tag(self, tag, relpath):
            '''Stores the tag for the image at relpath in the database.
            '''
            assert isinstance(tag, basestring) or isinstance(tag, unicode)
            try:
                imgpathset = self.tagmap[tag]
            except KeyError:
                self.tagmap[tag] = set()
                imgpathset = self.tagmap[tag]
            imgpathset.add(relpath)
            
        # access the database
        #-----------------------------------
        
        def has_tag(self, tag):
            '''Returns True if the database contains images tagged with this tag.
            '''
            return tag in self.tagmap
            
        def get_tags(self):
            '''Returns a set of all tags in this database.
            '''
            return set(self.tagmap.keys())
            
        def get_imgset_without_tags(self):
            '''Returns a set of paths to all untagged images.
            '''
            return self.untagged.copy()
            
        def get_imgset_with_tag(self, tag):
            '''Returns a set of paths to images, all of which are tagged
            '''
            try:
                imgpathset = self.tagmap[tag]
            except KeyError:
                imgpathset = set([])
            return imgpathset.copy()
            
        def get_imgset_with_all_tags(self, requiredtags):
            '''Returns a set of images that are all tagged with all specified tags.
            '''
            # for every required tag...
            pathsetlist = []
            for tag in requiredtags:
                # ...fetch a set of images with tag from imgdb
                pathset = self.get_imgset_with_tag(tag)
                pathsetlist.append(pathset)
            # find paths contained in all pathsets and therefore images tagged 
            # with all required tags
            try:
                pathset = pathsetlist.pop()
            except IndexError:
                msg = "none of the required tags is in this database! tags: %s"
                tagslog.warning(msg % sorted(requiredtags))
                return set([])
            requiredpathset = pathset.intersection(*pathsetlist)            
            return requiredpathset.copy()
            
        def remove_excluded_images(self, pathset, excludedtags):
            '''Removes all paths pointing to images with at least one excluded tag.
            '''
            # get a set of image paths that are tagged with any excluded tag
            excludedlist = [self.get_imgset_with_tag(t) for t in excludedtags]
            es = excludedlist.pop(0)
            excludedpaths = es.union(*excludedlist)
            # remove all imgpaths in excludedpaths from pathset
            pathset.difference_update(excludedpaths)
            return pathset
            
        def get_tags_per_character(self, character):
            """
            Returns a dict of tags as keys and amount of tags in the datebase
            character = character object
            4 Post-@ code review: Is this a stupid way of doing it? ==> It was...
            """
            tags = dict()
            all_tags = self.all_tags.copy()
            all_tags.add(character.id)
            images = self.get_imgset_with_tag(character.id)
            for img in images:
                tags_per_path = self.get_tags_per_path(img)
                for tag in tags_per_path:
                    if tag in all_tags:
                        tags[tag] = tags.get(tag, 0) + 1
            return tags
            
        def get_tags_per_path(self, path):    
            """
            Returns a set of tags got from the image path in the database
            path = path to a file
            """
            tags = set([])
            for key in self.tagmap:
                for tag in self.tagmap[key]:
                    if tag == path:
                        tags.add(key)
            return tags
            
        # dump the database
        #-----------------------------------
        def map_images_to_tags(self):
            '''Returns a dict of image path keys and sets of tags as values.
            '''
            imgmap = {}
            for tag in self.tagmap:
                imgpaths = self.tagmap[tag]
                for p in imgpaths:
                    try:
                        tagset = imgmap[p]
                    except KeyError:
                        imgmap[p] = set([])
                        tagset = imgmap[p]
                    tagset.add(tag)
            return imgmap
            
        def dump_json(self, targetfiles=[]):
            '''Dumps the tag information into tags.json files.
            
            targetfiles is a list of paths to files.
            If targetfiles is empty, a single tags.json file will be written to
            the game directory and will contain the complete database contents.
            '''
            # ensure that all target files have valid paths
            if targetfiles==[]:
                targets = {os.path.join(gamedir, "tags.json") : {}}
            else:
                targets = {}
                for p in targetfiles:
                    normpath = normalize_path(p)
                    targets[normpath] = {}
            for t in targets.keys():
                dirpath = os.path.dirname(t)
                if not os.path.exists(dirpath):
                    tagslog.error("directory does not exist: %s" % dirpath)
                    targets.pop(t)
            # separate database content by targetdir
            targetdirs = {}
            for t in targets:
                td = os.path.dirname(t)
                targetdirs[td] = t
            imgmap = self.map_images_to_tags()
            for imgpath in imgmap:
                taglist = sorted(imgmap[imgpath])
                normimgpath = normalize_path(imgpath)
                found = False
                for td in targetdirs:
                    if normimgpath.startswith(td):
                        targetfile = targetdirs[td]
                        targets[targetfile][imgpath] = taglist
                        found = True
                        break
                if not found:
                    tagslog.error("could not find target directory for %s" % imgpath)
            # write one JSON file per target directory
            for t in targets:
                imgmap = targets[t]
                tagslog.debug("writing tags to %s" % t)
                tagsfile = open(t, "w")
                json.dump(imgmap, tagsfile, indent=4, sort_keys=True)
                
        # get metadata
        #-----------------------------------
        def count_images(self):
            '''Returns the number of images in the database.
            '''
            images = self.get_all_images()
            return len(images)
            
        def get_all_images(self):
            imgsets = self.tagmap.values()
            allimages = set([])
            for i in imgsets:
                allimages = allimages.union(i)
            return allimages


    # enable logging
    tagslog = devlog.getChild("tags")
