import scripts.screens.base_screens as base_screens
import pygame_gui
import pygame
import scripts.global_vars as global_vars
from scripts.utility import update_sprite
from scripts.game_structure.image_cache import load_image
import scripts.game_structure.image_button as custom_buttons
from scripts.cat.cats import Cat
from scripts.cat.pelts import choose_pelt
from scripts.game_structure.image_cache import load_image

class CreationScreen(base_screens.Screens):

    def __init__(self, name):
        self.general_tab = None
        self.pattern_tab = None
        self.extras_tab = None
        self.cat_image = None
        self.back = None
        self.randomize = None
        self.clear = None
        self.done = None
        self.tab_background = None
        self.fur_length_select = None
        self.general_tab_button = None
        self.pattern_tab_button = None
        self.extras_tab_button = None
        self.color_select = None
        self.white_patches_select = None
        self.pose_select = None
        self.base_pelt_select = None
        self.cat_platform = None
        self.visable_tab = None
        self.dropdown_menus = {}
        self.checkboxes = {}
        self.labels = {}

        super().__init__(name)

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.general_tab_button:
                self.show_tab(self.general_tab)
                self.handle_page_switching(0)
            elif event.ui_element == self.pattern_tab_button:
                self.show_tab(self.pattern_tab)
                self.handle_page_switching(0)
            elif event.ui_element == self.extras_tab_button:
                self.show_tab(self.extras_tab)
                self.handle_page_switching(0)
            elif event.ui_element == self.next_page:
                self.handle_page_switching(1)
            elif event.ui_element == self.last_page:
                self.handle_page_switching(-1)
            elif event.ui_element == self.clear:
                global_vars.CREATED_CAT = Cat()
                self.build_dropdown_menus()
                self.update_checkboxes_and_disable_dropdowns()
                self.update_cat_image()
                self.update_platform()
            elif event.ui_element == self.randomize:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    shift_click = True
                else:
                    shift_click = False
                
                global_vars.CREATED_CAT.randomize_looks(just_pattern=shift_click)
                self.build_dropdown_menus()
                self.update_checkboxes_and_disable_dropdowns()
                self.update_cat_image()
                self.update_platform()
            elif event.ui_element == self.back:
                self.change_screen('start screen')
            # Here is where the cat creation checkboxes start.
            elif event.ui_element == self.checkboxes["tortie_checkbox"]:
                # Switch pelt to tortie.
                if global_vars.CREATED_CAT.pelt.name == "Tortie":
                    # Switch cat from tortie.
                    pelt = global_vars.CREATED_CAT.tortiebase.capitalize()

                    if pelt == "Single":
                        pelt = "SingleColour"

                    global_vars.CREATED_CAT.pelt = choose_pelt(
                        global_vars.CREATED_CAT.pelt.colour,
                        False,
                        pelt,
                        global_vars.CREATED_CAT.pelt.length
                    )

                else:
                    #Switch Cat to Tortie
                    global_vars.CREATED_CAT.pelt = choose_pelt(
                        global_vars.CREATED_CAT.pelt.colour,
                        False,
                        "Tortie",
                        global_vars.CREATED_CAT.pelt.length
                    )

                self.update_checkboxes_and_disable_dropdowns()
                self.update_cat_image()
            elif event.ui_element == self.checkboxes["hetero_eyes"]:

                # This will switch hetero eyes from off to on, and vis versa.
                if global_vars.CREATED_CAT.eye_colour2:
                    global_vars.CREATED_CAT.eye_colour2 = None
                else:
                    # We store the last eye color 2 in "stored eye color" for QOL reasons.
                    global_vars.CREATED_CAT.eye_colour2 = global_vars.CREATED_CAT.stored_eye_color_2

                self.build_dropdown_menus()
                self.update_checkboxes_and_disable_dropdowns()
                self.update_cat_image()
            elif event.ui_element == self.checkboxes["reverse"]:
                # This checkbox flips the car horizonally.
                if global_vars.CREATED_CAT.reverse:
                    global_vars.CREATED_CAT.reverse = False
                else:
                    global_vars.CREATED_CAT.reverse = True
                self.update_checkboxes_and_disable_dropdowns()
                self.update_cat_image()
            elif event.ui_element == self.checkboxes["shading"]:
                if global_vars.CREATED_CAT.shading:
                    global_vars.CREATED_CAT.shading = False
                else:
                    global_vars.CREATED_CAT.shading = True
                self.update_checkboxes_and_disable_dropdowns()
                self.update_cat_image()
            elif event.ui_element == self.checkboxes["paralyzed"]:
                if global_vars.CREATED_CAT.paralyzed:
                    global_vars.CREATED_CAT.paralyzed = False
                else:
                    global_vars.CREATED_CAT.paralyzed = True
                self.update_checkboxes_and_disable_dropdowns()
                self.update_cat_image()
            elif event.ui_element == self.checkboxes["sick"]:
                if global_vars.CREATED_CAT.not_working:
                    global_vars.CREATED_CAT.not_working = False
                else:
                    global_vars.CREATED_CAT.not_working = True
                self.update_checkboxes_and_disable_dropdowns()
                self.update_cat_image()
        
        
        # Here if where all the dropdown menu actions are handled. ---------------------------------------------
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.dropdown_menus["color_select"]:
                global_vars.CREATED_CAT.pelt.colour = global_vars.colors.inverse[event.text]
                global_vars.CREATED_CAT.tortiecolour = global_vars.colors.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["white_patches_select"]:
                global_vars.CREATED_CAT.white_patches = global_vars.white_patches.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["pelt_length_select"]:
                self.change_fur_length(event.text.lower())
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["pose_select"]:
                self.change_pose(event.text[-1])
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["pelt_select"]:

                selected = global_vars.pelt_options.inverse[event.text]

                if global_vars.CREATED_CAT.pelt.name == "Tortie":
                    if selected == "SingleColour":
                        selected = "single"
                    global_vars.CREATED_CAT.tortiebase = selected.lower()
                else:
                    global_vars.CREATED_CAT.pelt = choose_pelt(
                        global_vars.CREATED_CAT.pelt.colour,
                        False,
                        selected,
                        global_vars.CREATED_CAT.pelt.length
                    )
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["age_select"]:
                global_vars.CREATED_CAT.age = event.text.lower()
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["eye_color_1"]:
                global_vars.CREATED_CAT.eye_colour = global_vars.eye_colors.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["eye_color_2"]:
                global_vars.CREATED_CAT.eye_colour2 = global_vars.eye_colors.inverse[event.text]
                global_vars.CREATED_CAT.stored_eye_color_2 = global_vars.eye_colors.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["torte_patches_color"]:

                global_vars.CREATED_CAT.tortiecolour = global_vars.colors.inverse[event.text]
                global_vars.CREATED_CAT.stored_tortiecolour = global_vars.colors.inverse[event.text]

                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["torte_patches_pattern"]:

                global_vars.CREATED_CAT.tortiepattern = global_vars.tortie_patches_patterns.inverse[event.text]
                global_vars.CREATED_CAT.stored_tortiepattern = global_vars.tortie_patches_patterns.inverse[event.text]

                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["torte_patches_shape"]:

                global_vars.CREATED_CAT.pattern = global_vars.tortie_patches_shapes.inverse[event.text]
                global_vars.CREATED_CAT.stored_tortiepattern = global_vars.tortie_patches_shapes.inverse[event.text]

                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["skin_color_select"]:
                global_vars.CREATED_CAT.skin = global_vars.skin_colors.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["tint_select"]:
                global_vars.CREATED_CAT.tint = global_vars.tints.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["scar_1"]:
                global_vars.CREATED_CAT.scar_slot_list[0] = global_vars.scars.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["scar_2"]:
                global_vars.CREATED_CAT.scar_slot_list[1] = global_vars.scars.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["scar_3"]:
                global_vars.CREATED_CAT.scar_slot_list[2] = global_vars.scars.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["scar_4"]:
                global_vars.CREATED_CAT.scar_slot_list[3] = global_vars.scars.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["accessory"]:
                global_vars.CREATED_CAT.accessory = global_vars.accessories.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["lineart_select"]:
                if event.text == "StarClan":
                    global_vars.CREATED_CAT.dead = True
                    global_vars.CREATED_CAT.df = False
                elif event.text == "Dark Forest":
                    global_vars.CREATED_CAT.dead = True
                    global_vars.CREATED_CAT.df = True
                else:
                    global_vars.CREATED_CAT.dead = False
                    global_vars.CREATED_CAT.df = False
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["platform_select"]:
                global_vars.CREATED_CAT.platform = event.text
                self.update_platform()
            elif event.ui_element == self.dropdown_menus["white_patches_tint_select"]:
                global_vars.CREATED_CAT.white_patches_tint = global_vars.white_patches_tint.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["points_select"]:
                global_vars.CREATED_CAT.points = global_vars.points.inverse[event.text]
                self.update_cat_image()
            elif event.ui_element == self.dropdown_menus["vit_select"]:
                global_vars.CREATED_CAT.vitiligo = global_vars.vit.inverse[event.text]
                self.update_cat_image()

    def show_tab(self, container):
        for x in [self.pattern_tab, self.pattern_tab2, self.general_tab, self.extras_tab]:
            if x == container:
                x.show()
                self.visable_tab = x
            else:
                x.hide()
                
        tab_buttons = [((self.pattern_tab, self.pattern_tab2), self.pattern_tab_button),
                       ([self.general_tab], self.general_tab_button),
                       ([self.extras_tab], self.extras_tab_button)]
        
        for x in tab_buttons:
            if self.visable_tab in x[0]:
                x[1].disable()
            else:
                x[1].enable()
                    
    def handle_page_switching(self, direction: 1): 
        """Direction is next vs last page. 1 is next page, -1 is last page. 0 is no change (just update the buttons)  """
        if direction not in (1, 0, -1):
            return
        
        pages = [
            [self.pattern_tab, self.pattern_tab2]
        ]
        
        for x in pages:
            if self.visable_tab in x:
                index = x.index(self.visable_tab)
                new_index = index + direction
                if 0 <= new_index < len(x):
                    self.show_tab(x[new_index])
                    
                    if new_index == len(x) - 1:
                        self.last_page.enable()
                        self.next_page.disable()
                    elif new_index == 0:
                        self.next_page.enable()
                        self.last_page.disable()
                    else:
                        self.next_page.enable()
                        self.last_page.enable()
                            
                    return
                
        self.next_page.disable()
        self.last_page.disable()

    def update_platform(self):
        path = global_vars.platforms[
            global_vars.CREATED_CAT.platform
        ]

        if path:
            self.cat_platform.set_image(pygame.transform.scale(load_image(path), (480, 420)))
            self.cat_platform.show()
        else:
            self.cat_platform.hide()

    def screen_switches(self):
        update_sprite(global_vars.CREATED_CAT)

        if global_vars.CREATED_CAT.platform != "None":
            self.cat_platform = pygame_gui.elements.UIImage(pygame.Rect((160, 25), (480, 420)),
                                                            pygame.transform.scale(load_image(
                                                                global_vars.platforms[
                                                                    global_vars.CREATED_CAT.platform
                                                                ]),(480, 420)))
        else:
            self.cat_platform = pygame_gui.elements.UIImage(pygame.Rect((160, 25), (480, 420)),
                                                            global_vars.MANAGER.get_universal_empty_surface(),
                                                            visible=False)

        self.cat_image = pygame_gui.elements.UIImage(pygame.Rect((250, 25), (300, 300)),
                                                     pygame.transform.scale(global_vars.CREATED_CAT.sprite,
                                                                            (300, 300)))

        self.back = custom_buttons.UIImageButton(pygame.Rect((50, 25), (105, 30)), "",
                                                 object_id="#back_button")

        self.done = custom_buttons.UIImageButton(pygame.Rect((673, 25), (77, 30)), "",
                                                 object_id="#done_button")

        self.randomize = custom_buttons.UIImageButton(pygame.Rect((630, 291), (50, 50)), "",
                                                      object_id="#random_dice_button")

        self.clear = custom_buttons.UIImageButton(pygame.Rect((690, 291), (50, 50)), "",
                                                  object_id="#clear_button")

        # -----------------------------------------------------------------------------------------------------------
        # TAB BUTTONS -----------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------
        self.general_tab_button = custom_buttons.UIImageButton(pygame.Rect((50, 365), (100, 88)), "",
                                                               object_id="#general_tab_button")
        self.general_tab_button.disable()

        self.pattern_tab_button = custom_buttons.UIImageButton(pygame.Rect((50, 456), (100, 88)), "",
                                                               object_id="#pattern_tab_button")

        self.extras_tab_button = custom_buttons.UIImageButton(pygame.Rect((50, 547), (100, 88)), "",
                                                               object_id="#extra_tab_button")

        self.tab_background = pygame_gui.elements.UIImage(pygame.Rect((150, 350), (600, 300)),
                                                          load_image("resources/images/options.png"))
        
        # -----------------------------------------------------------------------------------------------------------
        # TAB CONTAINERS --------------------------------------------------------------------------------------------
        # -----------------------------------------------------------------------------------------------------------
        self.general_tab = pygame_gui.elements.UIScrollingContainer(pygame.Rect((150, 350), (600, 300)),
                                                                    global_vars.MANAGER)

        self.pattern_tab = pygame_gui.elements.UIScrollingContainer(pygame.Rect((150, 350), (600, 300)),
                                                                    global_vars.MANAGER,
                                                                    visible=False)
        
        self.pattern_tab2 = pygame_gui.elements.UIScrollingContainer(pygame.Rect((150, 350), (600, 300)),
                                                                    global_vars.MANAGER,
                                                                    visible=False)

        self.extras_tab = pygame_gui.elements.UIScrollingContainer(pygame.Rect((150, 350), (600, 300)),
                                                                   global_vars.MANAGER,
                                                                   visible=False)
        
        self.visable_tab = self.general_tab

        # ------------------------------------------------------------------------------------------------------------
        # Page Buttons -----------------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------
        self.last_page = custom_buttons.UIImageButton(pygame.Rect((334, 640), (34, 34)), "",
                                                      object_id="#last_page_button")
        self.next_page = custom_buttons.UIImageButton(pygame.Rect((534, 640), (34, 34)), "",
                                                      object_id="#next_page_button")
        self.last_page.disable()
        self.next_page.disable()


        # ------------------------------------------------------------------------------------------------------------
        # General Tab Labels -----------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------

        self.labels["Age"] = pygame_gui.elements.UILabel(pygame.Rect((20, 15), (150, 25)), "Age:",
                                                         container=self.general_tab,
                                                         object_id="#dropdown_label")

        self.labels["pose"] = pygame_gui.elements.UILabel(pygame.Rect((180, 15), (150, 25)), "Pose:",
                                                          container=self.general_tab,
                                                          object_id="#dropdown_label")

        self.labels["pelt_length"] = pygame_gui.elements.UILabel(pygame.Rect((20, 80), (150, 25)), "Pelt Length:",
                                                                 container=self.general_tab,
                                                                 object_id="#dropdown_label")

        self.labels["reversed"] = pygame_gui.elements.UILabel(pygame.Rect((226, 99), (-1, 25)), "Reversed",
                                                              container=self.general_tab,
                                                              object_id="#dropdown_label")

        self.labels["shading"] = pygame_gui.elements.UILabel(pygame.Rect((378, 99), (-1, 25)), "Shading",
                                                              container=self.general_tab,
                                                              object_id="#dropdown_label")

        self.labels["lineart"] = pygame_gui.elements.UILabel(pygame.Rect((340, 15), (150, 25)), "Lineart:",
                                                              container=self.general_tab,
                                                              object_id="#dropdown_label")
        
        self.labels["paralyzed"] = pygame_gui.elements.UILabel(pygame.Rect((55, 164), (-1, 25)), "Paralyzed",
                                                               container=self.general_tab,
                                                               object_id="#dropdown_label")
        
        self.labels["sick"] = pygame_gui.elements.UILabel(pygame.Rect((226, 164), (-1, 25)), "Sick",
                                                               container=self.general_tab,
                                                               object_id="#dropdown_label")

        # -------------------------------------------------------------------------------------------------------------
        # Pattern Tab Labels ------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------

        self.labels["color"] = pygame_gui.elements.UILabel(pygame.Rect((20, 15), (150, 25)), "Base Color:",
                                                           container=self.pattern_tab,
                                                           object_id="#dropdown_label")

        self.labels["base pattern"] = pygame_gui.elements.UILabel(pygame.Rect((185, 15), (150, 25)), "Base Pattern:",
                                                                  container=self.pattern_tab,
                                                                  object_id="#dropdown_label")

        self.labels["white_patches"] = pygame_gui.elements.UILabel(pygame.Rect((375, 15), (150, 25)), "White Patches:",
                                                                   container=self.pattern_tab,
                                                                   object_id="#dropdown_label")
        
        self.labels["points"] = pygame_gui.elements.UILabel(pygame.Rect((20, 70), (-1, 25)), "Point Markings:",
                                                                   container=self.pattern_tab,
                                                                   object_id="#dropdown_label")
        
        self.labels["vit"] = pygame_gui.elements.UILabel(pygame.Rect((220, 70), (-1, 25)), "Vitiligo:",
                                                                   container=self.pattern_tab,
                                                                   object_id="#dropdown_label")

        self.labels["eye color 1"] = pygame_gui.elements.UILabel(pygame.Rect((20, 125), (150, 25)), "Eye Color:",
                                                                 container=self.pattern_tab,
                                                                 object_id="#dropdown_label")

        self.labels["eye color 2"] = pygame_gui.elements.UILabel(pygame.Rect((385, 125), (150, 25)), "Second Eye Color:",
                                                                 container=self.pattern_tab,
                                                                 object_id="#dropdown_label")

        self.labels["tint"] = pygame_gui.elements.UILabel(pygame.Rect((200, 180), (150, 25)), "Tint:",
                                                          container=self.pattern_tab,
                                                          object_id="#dropdown_label")

        self.labels["white_patches_tint"] = pygame_gui.elements.UILabel(pygame.Rect((360, 180), (-1, 25)),
                                                                        "White Patches/Points Tint:",
                                                                        container=self.pattern_tab,
                                                                        object_id="#dropdown_label")

        self.labels["Skin Color"] = pygame_gui.elements.UILabel(pygame.Rect((20, 180), (150, 25)), "Skin Color:",
                                                                container=self.pattern_tab,
                                                                object_id="#dropdown_label")

        self.labels["hetero"] = pygame_gui.elements.UILabel(pygame.Rect((244, 145), (150, 25)), "Heterochromia",
                                                            container=self.pattern_tab,
                                                            object_id="#dropdown_label")

        
        
        # -------------------------------------------------------------------------------------------------------------
        # Pattern 2 Tab Labels ----------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------

        self.labels["tortie"] = pygame_gui.elements.UILabel(pygame.Rect((20, 15), (150, 25)), "Tortie",
                                                            container=self.pattern_tab2,
                                                            object_id="#dropdown_label")
        
        self.labels["Tortie Patches Color"] = pygame_gui.elements.UILabel(pygame.Rect((70, 15), (150, 25)),
                                                                          "Tortie Patches Color",
                                                                          container=self.pattern_tab2,
                                                                          object_id="#dropdown_label")

        self.labels["Tortie Patches pattern"] = pygame_gui.elements.UILabel(pygame.Rect((230, 15), (190, 25)),
                                                                          "Tortie Patches Pattern",
                                                                          container=self.pattern_tab2,
                                                                          object_id="#dropdown_label")

        self.labels["Tortie Patches shape"] = pygame_gui.elements.UILabel(pygame.Rect((420, 15), (190, 25)),
                                                                          "Tortie Patches Shape",
                                                                          container=self.pattern_tab2,
                                                                          object_id="#dropdown_label")

        # -------------------------------------------------------------------------------------------------------------
        # EXTRAS Tab Labels -------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------

        self.labels["scar_1"] = pygame_gui.elements.UILabel(pygame.Rect((20, 15), (150, 25)), "Scar 1:",
                                                            container=self.extras_tab,
                                                            object_id="#dropdown_label")

        self.labels["scar_2"] = pygame_gui.elements.UILabel(pygame.Rect((300, 15), (150, 25)), "Scar 2:",
                                                            container=self.extras_tab,
                                                            object_id="#dropdown_label")

        self.labels["scar_3"] = pygame_gui.elements.UILabel(pygame.Rect((20, 70), (150, 25)), "Scar 3:",
                                                            container=self.extras_tab,
                                                            object_id="#dropdown_label")

        self.labels["scar_4"] = pygame_gui.elements.UILabel(pygame.Rect((300, 70), (150, 25)), "Scar 4:",
                                                            container=self.extras_tab,
                                                            object_id="#dropdown_label")

        self.labels["accessory"] = pygame_gui.elements.UILabel(pygame.Rect((20, 125), (150, 25)), "Accessory:",
                                                               container=self.extras_tab,
                                                               object_id="#dropdown_label")

        self.labels["platform"] = pygame_gui.elements.UILabel(pygame.Rect((270, 125), (150, 25)), "Platform:",
                                                               container=self.extras_tab,
                                                               object_id="#dropdown_label")


        self.build_dropdown_menus()
        self.update_checkboxes_and_disable_dropdowns()        
        

    def update_cat_image(self):
        """ Updates the cat images and displays it. """
        update_sprite(global_vars.CREATED_CAT)
        self.cat_image.set_image(pygame.transform.scale(global_vars.CREATED_CAT.sprite, (300, 300)))

    def build_dropdown_menus(self):
        """ Creates all the dropdown menus. """

        for ele in self.dropdown_menus:
            self.dropdown_menus[ele].kill()
        self.dropdown_menus = {}

        # -------------------------------------------------------------------------------------------------------------
        # General Tab Contents ----------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------

        self.dropdown_menus["pelt_length_select"] = pygame_gui.elements.UIDropDownMenu(["Short", "Long"],
                                                                                       global_vars.CREATED_CAT.pelt.length.capitalize(),
                                                                                       pygame.Rect((20, 100), (150, 30)),
                                                                                       container=self.general_tab)

        self.dropdown_menus["pose_select"] = pygame_gui.elements.UIDropDownMenu(["Pose " + i for i in global_vars.poses[global_vars.CREATED_CAT.pelt.length][global_vars.CREATED_CAT.age]],
                                                                                 "Pose " +
                                                                                 global_vars.CREATED_CAT.current_poses[
                                                                                 global_vars.CREATED_CAT.age
                                                                                 ],
                                                                                 pygame.Rect((180, 35), (150, 30)),
                                                                                 container=self.general_tab)

        self.dropdown_menus["age_select"] = pygame_gui.elements.UIDropDownMenu(["Newborn", "Kitten", "Adolescent", "Adult", "Senior"],
                                                                               global_vars.CREATED_CAT.age.capitalize(),
                                                                               pygame.Rect((20, 35), (150, 30)),
                                                                               container=self.general_tab)

        if global_vars.CREATED_CAT.dead:
            if global_vars.CREATED_CAT.df:
                lineart = global_vars.lineart[2]
            else:
                lineart = global_vars.lineart[1]
        else:
            lineart = global_vars.lineart[0]

        self.dropdown_menus["lineart_select"] = pygame_gui.elements.UIDropDownMenu(global_vars.lineart,
                                                                                   lineart,
                                                                                   pygame.Rect((340, 35), (150, 30)),
                                                                                   container=self.general_tab)

        # -------------------------------------------------------------------------------------------------------------
        # Pattern Tab Contents ----------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------

        self.dropdown_menus["color_select"] = pygame_gui.elements.UIDropDownMenu(global_vars.colors.values(),
                                                                                 global_vars.colors[
                                                                                 global_vars.CREATED_CAT.pelt.colour],
                                                                                 pygame.Rect((20, 35), (155, 30)),
                                                                                 container=self.pattern_tab)


        current_base_pelt = global_vars.CREATED_CAT.pelt.name
        if current_base_pelt in ["Tortie", "Calcio"]:
            current_base_pelt = global_vars.CREATED_CAT.tortiebase.capitalize()
            if current_base_pelt == "Single":
                current_base_pelt = "SingleColour"

        self.dropdown_menus["pelt_select"] = pygame_gui.elements.UIDropDownMenu(global_vars.pelt_options.values(),
                                                                                global_vars.pelt_options[
                                                                                    current_base_pelt
                                                                                ],
                                                                                pygame.Rect((185, 35), (180, 30)),
                                                                                container=self.pattern_tab)

        if global_vars.CREATED_CAT.white_patches:
            white_patches = (global_vars.CREATED_CAT.white_patches.lower()).capitalize()
        else:
            white_patches = "None"
        self.dropdown_menus["white_patches_select"] = pygame_gui.elements.UIDropDownMenu(global_vars.white_patches.values(),
                                                                                         global_vars.white_patches[
                                                                                            global_vars.CREATED_CAT.white_patches
                                                                                         ],
                                                                                         pygame.Rect((375, 35), (190, 30)),
                                                                                         container=self.pattern_tab)
        
        self.dropdown_menus["points_select"] = pygame_gui.elements.UIDropDownMenu(global_vars.points.values(),
                                                                           global_vars.points[
                                                                               global_vars.CREATED_CAT.points
                                                                           ],
                                                                           pygame.Rect((20, 90), (190, 30)),
                                                                           container=self.pattern_tab)
        
        self.dropdown_menus["vit_select"] = pygame_gui.elements.UIDropDownMenu(global_vars.vit.values(),
                                                                        global_vars.vit[
                                                                            global_vars.CREATED_CAT.vitiligo
                                                                        ],
                                                                        pygame.Rect((220, 90), (190, 30)),
                                                                        container=self.pattern_tab)

        self.dropdown_menus["eye_color_1"] = pygame_gui.elements.UIDropDownMenu(global_vars.eye_colors.values(),
                                                                                global_vars.eye_colors[
                                                                                    global_vars.CREATED_CAT.eye_colour
                                                                                ],
                                                                                pygame.Rect((20, 145), (180, 30)),
                                                                                container=self.pattern_tab)

        if global_vars.CREATED_CAT.eye_colour2:
            eye_color_2 = global_vars.CREATED_CAT.eye_colour2
        else:
            eye_color_2 = global_vars.CREATED_CAT.eye_colour


        self.dropdown_menus["eye_color_2"] = pygame_gui.elements.UIDropDownMenu(global_vars.eye_colors.values(),
                                                                                global_vars.eye_colors[
                                                                                    eye_color_2
                                                                                ],
                                                                                pygame.Rect((385, 145), (180, 30)),
                                                                                container=self.pattern_tab)
        
        self.dropdown_menus["tint_select"] = pygame_gui.elements.UIDropDownMenu(global_vars.tints.values(),
                                                                                global_vars.tints[
                                                                                    global_vars.CREATED_CAT.tint
                                                                                ],
                                                                                pygame.Rect(((200, 200), (150, 30))),
                                                                                container=self.pattern_tab,
                                                                                object_id="#dropup")

        self.dropdown_menus["white_patches_tint_select"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.white_patches_tint.values(),
                                               global_vars.white_patches_tint[
                                                    global_vars.CREATED_CAT.white_patches_tint
                                               ],
                                               pygame.Rect(((360, 200), (205, 30))),
                                               container=self.pattern_tab,
                                               object_id="#dropup")

        self.dropdown_menus["skin_color_select"] = pygame_gui.elements.UIDropDownMenu(global_vars.skin_colors.values(),
                                                                                      global_vars.skin_colors[
                                                                                        global_vars.CREATED_CAT.skin
                                                                                      ],
                                                                                      pygame.Rect(((20, 200), (170, 30))),
                                                                                      container=self.pattern_tab,
                                                                                      object_id="#dropup")
        
        
        #------------------------------------------------------------------------------------------------------------
        # PATTERN TAB CONTENTS Page 2 -------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------------ 
        
         # Tortie Patches Color
        self.dropdown_menus["torte_patches_color"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.colors.values(),
                                               global_vars.colors[
                                                    global_vars.CREATED_CAT.tortiecolour
                                               ],
                                               pygame.Rect((70, 35), (150, 30)),
                                               container=self.pattern_tab2)

        self.dropdown_menus["torte_patches_pattern"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.tortie_patches_patterns.values(),
                                               global_vars.tortie_patches_patterns[
                                                  global_vars.CREATED_CAT.tortiepattern
                                               ],
                                               pygame.Rect((230, 35), (180, 30)),
                                               container=self.pattern_tab2)

        self.dropdown_menus["torte_patches_shape"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.tortie_patches_shapes.values(),
                                               global_vars.tortie_patches_shapes[
                                                   global_vars.CREATED_CAT.pattern
                                               ],
                                               pygame.Rect((420, 35), (150, 30)),
                                               container=self.pattern_tab2)

        #------------------------------------------------------------------------------------------------------------
        # EXTRAS TAB CONTENTS ---------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------------ 

        self.dropdown_menus["scar_1"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.scars.values(),
                                               global_vars.scars[
                                                   global_vars.CREATED_CAT.scar_slot_list[0]
                                               ],
                                               pygame.Rect((20, 35), (270, 30)),
                                               container=self.extras_tab)

        self.dropdown_menus["scar_2"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.scars.values(),
                                               global_vars.scars[
                                                   global_vars.CREATED_CAT.scar_slot_list[1]
                                               ],
                                               pygame.Rect((300, 35), (270, 30)),
                                               container=self.extras_tab)

        self.dropdown_menus["scar_3"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.scars.values(),
                                               global_vars.scars[
                                                   global_vars.CREATED_CAT.scar_slot_list[2]
                                               ],
                                               pygame.Rect((20, 90), (270, 30)),
                                               container=self.extras_tab)

        self.dropdown_menus["scar_4"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.scars.values(),
                                               global_vars.scars[
                                                   global_vars.CREATED_CAT.scar_slot_list[3]
                                               ],
                                               pygame.Rect((300, 90), (270, 30)),
                                               container=self.extras_tab)

        self.dropdown_menus["accessory"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.accessories.values(),
                                               global_vars.accessories[
                                                   global_vars.CREATED_CAT.accessory
                                               ],
                                               pygame.Rect((20, 145), (240, 30)),
                                               container=self.extras_tab)

        self.dropdown_menus["platform_select"] = \
            pygame_gui.elements.UIDropDownMenu(global_vars.platforms.keys(),
                                               global_vars.CREATED_CAT.platform,
                                               pygame.Rect((270, 145), (270, 30)),
                                               container=self.extras_tab)

    def update_checkboxes_and_disable_dropdowns(self):
        """ This function updates the state of the checkboxes, and also disables any dropdown menus that
            need to be disabled. """
        for ele in self.checkboxes:
            self.checkboxes[ele].kill()
        self.checkboxes = {}
        
        # -------------------------------------------------------------------------------------------------------------
        # General Tab -------------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------
        
        #Shading
        if global_vars.CREATED_CAT.shading:
            self.checkboxes["shading"] = custom_buttons.UIImageButton(pygame.Rect((340, 95), (34, 34)),
                                                                      "",
                                                                      object_id="#checked_checkbox",
                                                                      container=self.general_tab)
        else:
            self.checkboxes["shading"] = custom_buttons.UIImageButton(pygame.Rect((340, 95), (34, 34)),
                                                                      "",
                                                                      object_id="#unchecked_checkbox",
                                                                      container=self.general_tab)
            
        # Reversed
        if global_vars.CREATED_CAT.reverse:
            self.checkboxes["reverse"] = custom_buttons.UIImageButton(pygame.Rect((190, 95), (34, 34)),
                                                                      "",
                                                                      object_id="#checked_checkbox",
                                                                      container=self.general_tab)
        else:
            self.checkboxes["reverse"] = custom_buttons.UIImageButton(pygame.Rect((190, 95), (34, 34)),
                                                                      "",
                                                                      object_id="#unchecked_checkbox",
                                                                      container=self.general_tab)
        
        # Paralyzed
        if global_vars.CREATED_CAT.paralyzed:
            self.checkboxes["paralyzed"] = custom_buttons.UIImageButton(pygame.Rect((20, 160), (34, 34)),
                                                                        "",
                                                                        object_id="#checked_checkbox",
                                                                        container=self.general_tab)
        else:
            self.checkboxes["paralyzed"] = custom_buttons.UIImageButton(pygame.Rect((20, 160), (34, 34)),
                                                                        "",
                                                                        object_id="#unchecked_checkbox",
                                                                        container=self.general_tab)
            
        # Sick
        if global_vars.CREATED_CAT.not_working:
            self.checkboxes["sick"] = custom_buttons.UIImageButton(pygame.Rect((190, 160), (34, 34)),
                                                                   "",
                                                                   object_id="#checked_checkbox",
                                                                   container=self.general_tab)
        else:
            self.checkboxes["sick"] = custom_buttons.UIImageButton(pygame.Rect((190, 160), (34, 34)),
                                                                   "",
                                                                   object_id="#unchecked_checkbox",
                                                                   container=self.general_tab)

        # -------------------------------------------------------------------------------------------------------------
        # Pattern Tab -------------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------


        # Heterochromia
        if global_vars.CREATED_CAT.eye_colour2:
            self.checkboxes["hetero_eyes"] = custom_buttons.UIImageButton(pygame.Rect((210, 140), (34, 34)),
                                                                          "",
                                                                          object_id="#checked_checkbox",
                                                                          container=self.pattern_tab)
            self.dropdown_menus["eye_color_2"].enable()
        else:
            self.checkboxes["hetero_eyes"] = custom_buttons.UIImageButton(pygame.Rect((210, 140), (34, 34)),
                                                                          "",
                                                                          object_id="#unchecked_checkbox",
                                                                          container=self.pattern_tab)
            self.dropdown_menus["eye_color_2"].disable()
            
        # -------------------------------------------------------------------------------------------------------------
        # Pattern 2 Tab -----------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------
        
         # Tortie checkbox
        if global_vars.CREATED_CAT.pelt.name == "Tortie":
            self.checkboxes["tortie_checkbox"] = custom_buttons.UIImageButton(pygame.Rect((25, 35), (34, 34)),
                                                                              "",
                                                                              object_id="#checked_checkbox",
                                                                              container=self.pattern_tab2)
            self.dropdown_menus["torte_patches_color"].enable()
            self.dropdown_menus["torte_patches_pattern"].enable()
            self.dropdown_menus["torte_patches_shape"].enable()
        else:
            self.checkboxes["tortie_checkbox"] = custom_buttons.UIImageButton(pygame.Rect((25, 35), (34, 34)),
                                                                              "",
                                                                              object_id="#unchecked_checkbox",
                                                                              container=self.pattern_tab2)
            self.dropdown_menus["torte_patches_color"].disable()
            self.dropdown_menus["torte_patches_pattern"].disable()
            self.dropdown_menus["torte_patches_shape"].disable()
        
        # -------------------------------------------------------------------------------------------------------------
        # Extras Tab --------------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------------------------------------

    def change_pose(self, pose: str=None):
        # Changes the pose from 1, 2, or 3
        if pose:
            # Change the sprite number.
            global_vars.CREATED_CAT.cat_sprites[global_vars.CREATED_CAT.age] = global_vars.poses[
                global_vars.CREATED_CAT.pelt.length][global_vars.CREATED_CAT.age][pose]

            # Adjust tracked poses.
            global_vars.CREATED_CAT.current_poses[global_vars.CREATED_CAT.age] = pose



    def change_fur_length(self, fur_length: str=None):
        if fur_length:
            global_vars.CREATED_CAT.pelt.length = fur_length

            # Change all poses for all ages. 
            for age in global_vars.CREATED_CAT.current_poses:
                # This is such a mess of dictionary lookups.
                global_vars.CREATED_CAT.cat_sprites[age] = global_vars.poses[
                    fur_length][age][global_vars.CREATED_CAT.current_poses[age]]

    def exit_screen(self):
        self.back.kill()
        self.back = None

        self.done.kill()
        self.done = None

        self.cat_platform.kill()
        self.cat_platform = None

        self.randomize.kill()
        self.randomize = None

        self.clear.kill()
        self.clear = None

        self.cat_image.kill()
        self.cat_image = None

        # Tabs
        self.general_tab_button.kill()
        self.general_tab_button = None

        self.pattern_tab_button.kill()
        self.pattern_tab_button = None

        self.extras_tab_button.kill()
        self.pattern_tab_button = None

        self.tab_background.kill()
        self.tab_background = None

        # TAB CONTAINERS
        self.general_tab.kill()
        self.general_tab = None

        self.pattern_tab.kill()
        self.pattern_tab = None

        self.extras_tab.kill()
        self.extras_tab = None

        self.labels = {}
        self.dropdown_menus = {}
        self.checkboxes = {}

class DoneScreen(base_screens.Screens):

    def __init__(self, name):
        self.save_dict = {}
        super().__init__(name)

    def handle_event(self, event):
        pass

    def screen_switches(self):
        self.save_dict = global_vars.CREATED_CAT.generate_save_file()

    def exit_screen(self):
        pass

    def save_png(self, path):
        pass


class SaveCodeScreen(base_screens.Screens):

    def __init__(self, name):

        super().__init__(name)
        
        


