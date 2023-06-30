import cv2
import numpy as np
import math


class PersonLooking:
    """Estimate head pose according to the facial landmarks"""

    def __init__(self, names, frameRate):

        # Schematic parameters
        self.schemaPos = (960, 540) #initial position
        self.r = 175 #radius of the schema circle
        
        self.circle_color = (255, 100, 0)
        self.names_color = (255, 102, 255)
        self.line_color = (1, 1, 1)
        self.graduation_color = (255, 255, 255)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

        self.colorCircle = [(0, 128, 255),
                            (0, 255, 255),
                            (0, 255, 0),
                            (255, 255, 0),
                            (255, 0, 0),
                            (255, 0, 255),
                            (128, 128, 128)]


        self.time = [0 for x in names]
        self.personLooking = [None for x in names]

        self.frameRate = frameRate
    


    def get_colors(self):
        return self.colorCircle



    def change_position(self, x, y):
        self.schemaPos = (x, y)



    def persons_position_in_frame(self, angles, numberPerson):

        # Persons Positions
        self.personsFrame = {}

        # Persons positions in the frame
        for i in range(0, numberPerson):
            if(angles[i] < 180):
                x = int(angles[i] * 1920 / 180)
                y = 500
            else:
                x = int((angles[i] - 180) * 1920 / 180)
                y = 950
            self.personsFrame[i, 0] = x
            self.personsFrame[i, 1] = y
            
        return self.personsFrame



    def draw_on_video(self, frame, names, framePrecision, numberPerson, angles):
        
        # Schema graduation
        cv2.line(frame, (0, 15), (1920, 15), self.graduation_color, 2)
        cv2.line(frame, (0, 550), (1920, 550), self.graduation_color, 2)

        for i in range(0, 181, 10):
            x1 = int(i*1920/181)
            x2 = int((i-5) *1920/181)

            cv2.line(frame, (x1, 10), (x1, 20), self.graduation_color, 2)
            cv2.line(frame, (x2, 13), (x2, 17), self.graduation_color, 2)

            cv2.line(frame, (x1, 545), (x1, 555), self.graduation_color, 2)
            cv2.line(frame, (x2, 548), (x2, 552), self.graduation_color, 2)

            cv2.putText(frame, str(i), (x1 - 15, 40), self.font, 0.6, self.graduation_color, 2)
            cv2.putText(frame, str(i + 180), (x1 - 15, 575), self.font, 0.6, self.graduation_color, 2)
    
        # Draw boxs with names
        for i in range(0, numberPerson):
            if(angles[i] < 180):
                cv2.rectangle(frame, ((self.personsFrame[i, 0] - framePrecision), 15),
                            ((self.personsFrame[i, 0] + framePrecision), 530), (0, 0, 255), 4)
            else:
                cv2.rectangle(frame, ((self.personsFrame[i, 0] - framePrecision), 550),
                            ((self.personsFrame[i, 0] + framePrecision), 1060), (0, 0, 255), 4)

            cv2.putText(frame, names[i], (self.personsFrame[i, 0] - framePrecision + 10, self.personsFrame[i, 1] - 50), self.font, 1, self.names_color, 2, cv2.LINE_4)




    def draw_schema(self, frame, names, numberPerson, angles):

        # Draw rond table
        cv2.circle(frame, self.schemaPos, self.r, (255, 255, 255), -1)

        # Draw camera
        cv2.circle(frame, self.schemaPos, 5, (1, 1, 1), -1)

        # Draw graduation on schema
        for i in range(0, 180, 10):
            x1 = - int(self.r * math.cos((i * 3.14) / 180)) + self.schemaPos[0]
            y1 = - int(self.r * math.sin((i * 3.14) / 180)) + self.schemaPos[1]

            x2 = - int(self.r * math.cos(((i + 180) * 3.14) / 180)) + self.schemaPos[0]
            y2 = - int(self.r * math.sin(((i + 180) * 3.14) / 180)) + self.schemaPos[1]

            cv2.circle(frame, (x1, y1), 3, (0, 0, 255), -1)
            cv2.circle(frame, (x2, y2), 3, (0, 0, 255), -1)

            cv2.putText(frame, str(i), (x1 - 10, y1 - 10), self.font, 0.3, (0, 0, 255), 1)
            cv2.putText(frame, str(i + 180), (x2 - 10, y2 - 10), self.font, 0.3, (0, 0, 255), 1)

        # Persons positions in the circle
        self.personsCircle = {}

        for i in range(0, numberPerson):
            x = - int(self.r * math.cos((angles[i] * 3.14) / 180)) + self.schemaPos[0]
            y = - int(self.r * math.sin((angles[i] * 3.14) / 180)) + self.schemaPos[1]
            self.personsCircle[i, 0] = x
            self.personsCircle[i, 1] = y
            cv2.circle(frame, (self.personsCircle[i, 0], self.personsCircle[i, 1]), 18, self.colorCircle[i], -1)
            cv2.putText(frame, names[i], (self.personsCircle[i, 0] - 5, self.personsCircle[i, 1] + 5), self.font, 0.4, self.names_color, 2, cv2.LINE_4)
            


    def rotation_matrix_to_angles(self, rotation_matrix):
        """
        Source: https://github.com/shenasa-ai/head-pose-estimation
        Calculate Euler angles from rotation matrix.
        :param rotation_matrix: A 3*3 matrix with the following structure
        [Cosz*Cosy  Cosz*Siny*Sinx - Sinz*Cosx  Cosz*Siny*Cosx + Sinz*Sinx]
        [Sinz*Cosy  Sinz*Siny*Sinx + Sinz*Cosx  Sinz*Siny*Cosx - Cosz*Sinx]
        [  -Siny             CosySinx                   Cosy*Cosx         ]
        :return: Angles in degrees for each axis
        """
        x = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
        y = math.atan2(-rotation_matrix[2, 0], math.sqrt(rotation_matrix[0, 0] ** 2 +rotation_matrix[1, 0] ** 2))
        z = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
        return np.array([x, y, z]) * 180. / math.pi



    def draw_result(self, frame, yaw, pitch, i, framePrecision, angles, names):

        # Show the yaw & pitch values
        cv2.putText(frame, 'yaw: ' + str(yaw), (self.personsFrame[i, 0] - framePrecision + 10, self.personsFrame[i, 1] - 15), self.font, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, 'pitch: ' + str(pitch), (self.personsFrame[i, 0] - framePrecision + 10, self.personsFrame[i, 1] + 15), self.font, 0.6, (0, 255, 255), 2)

        # Draw the lines of vision on the schema
        length = 100 # line length

        x2 = int(self.personsCircle[i, 0] + length * math.cos((angles[i] - yaw) * 3.14 / 180.0))
        y2 = int(self.personsCircle[i, 1] + length * math.sin((angles[i] - yaw) * 3.14 / 180.0))

        cv2.line(frame, (self.personsCircle[i, 0], self.personsCircle[i, 1]), (x2, y2), self.line_color, 3)

        # Re draw the circle & name of persons so that the line gets under it
        cv2.circle(frame, (self.personsCircle[i, 0], self.personsCircle[i, 1]), 18, self.colorCircle[i], -1)
        cv2.putText(frame, names[i], (self.personsCircle[i, 0] - 5, self.personsCircle[i, 1] + 5), self.font, 0.4, self.names_color, 2, cv2.LINE_4)



    def looking_position(data, i, numberPerson, last_look):
        lookingAngleX = data[str(i+1)]["angles"][0] + 180 - 2 * data[str(i+1)]["yaw"]
        lookingAngleY = data[str(i+1)]["angles"][1] + 90 - 2 * data[str(i+1)]["pitch"]

        if(lookingAngleX > 360):
            lookingAngleX = lookingAngleX - 360
        if (lookingAngleY > 180):
            lookingAngleY = lookingAngleY - 180

        # This version tells which person you are most possibly looking at
        old_min_x = 360
        old_min_y = 180
        previous_sum= old_min_x*2+old_min_y

        for l in range(0, numberPerson):
            if l != i:
                new_min_x = abs(lookingAngleX - data[str(l+1)]["angles"][0])
                new_min_y = abs(lookingAngleY - data[str(l+1)]["angles"][1])
                if ((new_min_x*2+new_min_y) < previous_sum):
                    old_min_x = new_min_x
                    old_min_y = new_min_y
                    previous_sum= old_min_x*2+old_min_y
                    mostPossPerson = l+1
        looking_user= str(mostPossPerson)
        
        # Person looking text
        if(-30 <= old_min_x <= 30 and -30 <= old_min_y <= 30):
            text = "Sure"
        elif(-60 <= old_min_x < -30 or 30 < old_min_x <= 60 and -60 <= old_min_y < -30 or 30 < old_min_y <= 60):
            text = "Possible"
        else:
            text = "Not Sure"

        # Calc time looking
        if last_look[str(i+1)][0] == looking_user:
            lookingtime = last_look[str(i+1)][1]+1
        else:
            lookingtime= 0
        
        #lookingtime= int(self.time[i]) #/(self.frameRate * 10))
        return (looking_user,text,old_min_x,old_min_y,lookingtime)