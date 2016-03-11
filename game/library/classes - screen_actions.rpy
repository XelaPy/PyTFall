init -10 python:
    class NullAction(Action):
        """
        Overrides the NullAction action to allow for the action to present an insensitive button.
        """
        
        def __init__(self, insensitive=False, selected=False):
            """
            Creates a new NullAction.
            insensitive = Whether to show an insensitive button.
            """
            self.ins = insensitive
            self.sel = selected
        
        def __call__(self):
            """
            Nothing.
            """
            return
        
        def get_selected(self):
            """
            Whether the button should be selected.
            """
            return self.sel
        
        def get_sensitive(self):
            """
            Whether the button should be insensitive.
            """
            return not self.ins
        
    
    class SetField(Action, FieldEquality):
        """
        Overrides the SetField action to allow for property creation in certain useage cases.
        Meant for setting properties in the stage, not within other objects.
        """
        
        # Used for FieldEquality, ignore
        identity_fields = [ "container", "value" ]
        equality_fields = [ "value" ]
        
        def __init__(self, container, name, value, create=False):
            """
            Creates a new SetField instance.
            container = The container of the property to set.
            name = The name of the property.
            value = The value to set to.
            create = Whether to create the property if it doesn't already exist.
            """
            self.container = container
            self.name = name
            self.value = value
            self.create = create
        
        def __call__(self):
            """
            Functions the action.
            """
            if hasattr(self.container, self.name):
                setattr(self.container, self.name, self.value)
            
            elif self.create:
                setattr(self.container, self.name, self.value)
            
            else:
                raise AttributeError("Property \"%s\" does not exist in container \"%s\"."%(self.name, self.container))
            
            renpy.restart_interaction()
        
        def get_selected(self):
            """
            Whether the property in container equals the value.
            """
            return getattr(self.container, self.name, None) == self.value
            
            
    # Menu extensions:
    class MenuExtensionAction(Action):
        def __init__(self, actions, extra_action=None):
            if extra_action:
                if "return" in actions:
                    actions.remove("return")
                actions.append(extra_action)
            self.actions = actions
        def __call__(self):
            for callable in self.actions:
                callable()
