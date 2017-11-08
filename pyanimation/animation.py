#!/usr/bin/python
import pygame


class Animation:
    def __init__(self, initial_action, speed=15):
        self.action = initial_action
        self.x = 250
        self.y = 200
        self.ani_speed = speed
        self.ani_pos = 0
        self.ani_max = 0
        self.sprite_sheet = None
        self.animation = []
        self.dict_of_rects = {}
        self.animation_speed = {}
        self.local_action = ""
        self.manual_list = []
        self.hold_state = {}
        self.facing_right = True

    def rect_list(self, xo, yo, lx, ly, n, rows):
        """
        Build a list of rectangles sprites
        xo,yo initial points at the top left corner
        lx,ly length of sprites
        n number of sprites
        """
        rect = []
        for row in range(rows):
            for i in range(n):
                rect.append(pygame.Rect(xo+lx*i, yo+ly*row, lx, ly))
        return rect

    def insert_frame(self, xo, yo, lx, ly):
        """
        Insert frame by frame manually
        xo,yo initial points at the top left corner
        lx,ly length of sprites
        """
        self.manual_list.append(pygame.Rect(xo, yo, lx, ly))

    def build_animation(self, action, hold=False, speed=15):
        """
        Build Animation from the inserted frames
        and sets a name for the animation
        """
        self.animation_speed[action] = speed
        self.dict_of_rects[action] = self.manual_list
        self.manual_list = []
        self.hold_state[action] = hold

    def erase_positions(self, action, indexes):
        """
        Erase a rectangle sprite of the self-generated rectangle list
        """
        indexes.sort()
        indexes.reverse()
        local_list = self.dict_of_rects[action]
        for item in indexes:
            local_list.pop(item)
        self.dict_of_rects[action] = local_list

    def repeat_position(self, action, ntimes, indexes):
        """
        Repeat a rectangle sprite of the self-generated rectangle list
        """
        indexes.sort()
        local_list = self.dict_of_rects[action]
        # append at the end n times
        while ntimes != 0:
            for item in indexes:
                local_list.append(local_list[item])
            ntimes = ntimes - 1

    def load_sprites(self, image_path):
        """
        Load the sprites image file
        """
        import os
        image_path = os.path.abspath(image_path)
        self.sprite_sheet = (pygame.image.load(image_path).convert_alpha())

    def create_animation(self, xo, yo, lx, ly, n, action, hold=False, speed=15, rows=1):
        """
        Create an intire animation and sets a label to the animation
        xo,yo: initial points at the top left corner
        lx,ly: length of sprites
        n: number of frames per row
        hold: True to run animation just once or false to keep running
        """
        self.animation_speed[action] = speed
        self.dict_of_rects[action] = self.rect_list(xo, yo, lx, ly, n, rows)
        self.hold_state[action] = hold

    def frame_list(self, action):
        return self.dict_of_rects[action]

    def run(self, action):
        """It allows the animation to start over each time it's called"""
        self.action = action
        if self.ani_pos == self.ani_max:
            self.ani_pos = 0

    def flip_animation(self, frame_list):
        """Flips animation to left or right"""
        try:
            cropped = self.sprite_sheet.subsurface(frame_list[self.ani_pos]).copy()
        except IndexError:
            print("List index out of range ocurred")
            self.ani_pos = 0
            cropped = self.sprite_sheet.subsurface(frame_list[self.ani_pos]).copy()
        if self.facing_right is False:
            cropped = pygame.transform.flip(cropped, True, False)
        return cropped

    def update_surface(self):
        """
        Run and update the animation
        Also flips the animation to righ or left as requested
        """
        # new animation starts at 0
        if self.local_action != self.action:
            self.ani_pos = 0
        self.local_action = self.action
        frame_list = self.frame_list(self.action)
        self.ani_max = len(frame_list)-1
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.ani_speed = self.animation_speed[self.action]
            # non-stop animation
            if self.ani_pos == self.ani_max and self.hold_state[self.action] is False:
                self.ani_pos = 0
            elif self.ani_pos < self.ani_max:
                self.ani_pos += 1
        subsurface = self.flip_animation(frame_list)
        return subsurface
