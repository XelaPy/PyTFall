init -11 python:
    # ------------------ Tagging system related: ==> And no londer in use!
    def locate_files(pattern, root, recursive=True):
        # No longer used...
        '''Locate all files matching pattern in and below the root directory.

        If recursive is False, only the root directory is searched.
        Example patterns:
            *.txt       matches all txt files
        '''
        toppath = os.path.abspath(root)
        # topdown must be True
        for path, dirs, files in os.walk(toppath, topdown=True):
            if not recursive: dirs[:] = []
            # dirs = [] rebinds dirs to a newly created list, leaving the old
            # one (to which os.walk() still holds a reference) unaltered.
            # The line dirs[:] = [] accesses the content of dirs and replaces it
            # with an empty list
            # src: http://bytes.com/topic/python/answers/28771-os-walk-walks-too-much
            for filename in fnmatch.filter(files, pattern):
                yield os.path.join(path, filename)

    def generate_tags():
        # No longer used...
        '''Generate tag information from image filenames.

        The function returns a dictionary of tags as keys and lists of relative
        image paths as values.
        '''
        tagmap = {}
        # determine the absolute path to content/chars at runtime
        charsdir = os.path.join(gamedir, "content", "chars")
        # determine the name of the character
        datafiles = locate_files("data.xml", charsdir)
        for df in datafiles:
            dirpath = os.path.dirname(df)
            for chardirname in os.listdir(dirpath):
                chardirpath = os.path.join(dirpath, chardirname)
                # find all images in the directory tree rooted here
                images = []
                for abspath in locate_files("*.jpg", chardirpath):
                    images.append(abspath)
                for abspath in locate_files("*.png", chardirpath):
                    images.append(abspath)
                # generate tags from the filename
                for abspath in images:
                    fullfilename = os.path.basename(abspath)
                    filename, ext = os.path.splitext(fullfilename)
                    # determine the relative path to the file in renpy notation
                    relpath = normalize_path(abspath, start=gamedir)
                    renpypath = relpath.replace("\\", "/")
                    # split at whitespace and assume the first word is the tag
                    tag = filename.split()[0]
                    tag = tag.lower()
                    try:
                        tagmap[tag].append(renpypath)
                    except KeyError:
                        tagmap[tag] = [renpypath]
                    # add character name
                    try:
                        tagmap[chardirname].append(renpypath)
                    except KeyError:
                        tagmap[chardirname] = [renpypath]
        msg = "generated the following tags for images in 'content/chars':\n%s"
        tagslog.debug(msg % ", ".join(sorted(tagmap.keys())))
        return tagmap

    # def rebuild_tagsjson():
    #     # No longer used...
    #     '''Rebuilds the JSON files storing the image tags.
    #     '''
    #     tagdb = TagDatabase()
    #     charsdir = os.path.join(gamedir, "content", "chars")
    #     datafiles = locate_files("data.xml", charsdir)
    #     # generate tags based on filename
    #     tagmap = generate_tags()
    #     for tag in tagmap:
    #         imgpaths = tagmap[tag]
    #         for p in imgpaths:
    #             tagdb.add_tag(tag, p)
    #     # dump the tags in the database into their respective JSON file
    #     targetdirs = [os.path.dirname(df) for df in datafiles]
    #     targets = [os.path.join(td, "tags.json") for td in targetdirs]
    #     tagdb.dump_json(targets)

    def normalize_path(path, start=""):
        # No longer used...
        # This is the same as renpy.loader.transfn so it is useless anyway.
        '''Returns a filesystem path following the conventions of the local OS.

        If start is empty, an absolute path will be returned.
        If start is not empty, a path relative to start will be returned.
        '''
        path = os.path.normpath(path)
        # determine an absolute version of path
        if os.path.isabs(path):
            abspath = path
        else:
            abspath = os.path.normpath(os.path.join(gamedir, path))
        # return the normalized path
        if start=="":
            normpath = abspath
        else:
            startpath = os.path.normpath(start)
            normpath = os.path.relpath(abspath, start=startpath)
        return normpath
