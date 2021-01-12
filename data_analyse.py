import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
"""
landmarks_eyes_left = np.arange(36,42)
landmarks_eyes_rigth = np.arange(42,48)


def compute_ear():



df = pd.read_csv("data/landmarks.csv")

df["ear_l"] = (df["euclid_dist_38_42_l"]+df["euclid_dist_39_41_l"])/(2*df["euclid_dist_37_40_l"])
df["ear_r"] = (df["euclid_dist_44_48_r"]+df["euclid_dist_45_47_r"])/(2*df["euclid_dist_43_46_r"])
df["ear"] = (df["ear_l"]+df["ear_r"])/2

df[('ear')].plot()


plt.xlabel("frame")
plt.ylabel("eye aspect ratio")
plt.show()
"""

VIDEOS_INFOS_PATH = "data/data_out/videos_infos.csv"

def parse_path_to_name(path):
    name_with_extensions = path.split("/")[-1]
    name = name_with_extensions.split(".")[0]
    return name

class AnalyseData():
    def __init__(self, csv_path):
        self.df_landmarks = pd.read_csv(csv_path).rename(columns={"Unnamed: 0" : "frame"})
        self.df_measure = pd.DataFrame( self.df_landmarks["frame"])
        self.df_videos_infos = pd.read_csv(VIDEOS_INFOS_PATH)
        self.video_name = parse_path_to_name(csv_path)

    def measure_euclid_dist(self, landmarks_1, landmarks_2):
        x_1 = "landmarks_"+str(landmarks_1)+"_x"
        y_1 = "landmarks_"+str(landmarks_1)+"_y"
        x_2 = "landmarks_"+str(landmarks_2)+"_x"
        y_2 = "landmarks_"+str(landmarks_2)+"_y"
        a = self.df_landmarks[[x_1,y_1]].rename(columns={x_1 : "x", y_1 :"y"})
        b = self.df_landmarks[[x_2,y_2]].rename(columns={x_2 : "x", y_2 :"y"})
        return (a-b).apply(np.linalg.norm,axis=1)


   #not finished
    def measure_yawning_frequency(self):
        self.df_measure["mouth"] = (self.measure_euclid_dist(62,68) + self.measure_euclid_dist(63,67) + self.measure_euclid_dist(64,68)) / (2*self.measure_euclid_dist(61,65))
        #find the value that indicates a yawning
        #if this value is reached, add +1 on the frequency count

    #not finished
    def measure_blinking(self):
        self.df_measure["eye_l"] = (self.measure_euclid_dist(38,42) + self.measure_euclid_dist(39,41)) / (2*self.measure_euclid_dist(37,40))
        self.df_measure["eye_r"] = (self.measure_euclid_dist(44,48) + self.measure_euclid_dist(45,47)) / (2*self.measure_euclid_dist(43,46))
        self.df_measure["eye"]   = (self.df_measure["eye_r"] +self.df_measure["eye_l"])/2
        #when this measurement equals 0, we have a blink
        #if this happens, we add +1 on the blinking count

    def measure_blinking2(self):
        self.df_measure["eye_l"] = (self.measure_euclid_dist(38,42) + self.measure_euclid_dist(39,41)) / (2*self.measure_euclid_dist(37,40))
        #self.df_measure["eye_r"] = (self.measure_euclid_dist(45,47))
        #self.df_measure["eye2"]   = (self.df_measure["eye_r"] +self.df_measure["eye_l"])/2
        #when this measurement equals 0, we have a blink
        #if this happens, we add +1 on the blinking count

    def measure_blinking3(self):
        self.df_measure["eye_r"] = (self.measure_euclid_dist(44,48) + self.measure_euclid_dist(45,47)) / (2*self.measure_euclid_dist(43,46))
        #self.df_measure["eye2"]   = (self.df_measure["eye_r"] +self.df_measure["eye_l"])/2
        #when this measurement equals 0, we have a blink
        #if this happens, we add +1 on the blinking count


    def measure_ear(self): # calculate
        self.df_measure["ear_l"] = (self.measure_euclid_dist(38,42) + self.measure_euclid_dist(39,41)) / (2*self.measure_euclid_dist(37,40))
        self.df_measure["ear_r"] = (self.measure_euclid_dist(44,48) + self.measure_euclid_dist(45,47)) / (2*self.measure_euclid_dist(43,46))
        self.df_measure["ear"]   = (self.df_measure["ear_r"] +self.df_measure["ear_l"])/2

    def measure_eyebrows_nose(self):
        self.df_measure["eyebrowns_nose_l"] = (self.measure_euclid_dist(20,32))
        self.df_measure["eyebrowns_nose_r"] = (self.measure_euclid_dist(25,36))
        self.df_measure["eyebrowns_nose"]   = (self.df_measure["eyebrowns_nose_r"] + self.df_measure["eyebrowns_nose_r"])/ 2
        #print(self.df_measure)

    def measure_perclos(self, percent, threshold):
        self.df_measure["eye_area_l"] = (self.measure_euclid_dist(37, 40) / 2) * ((self.measure_euclid_dist(38, 42) + self.measure_euclid_dist(39,41)) /2) * np.pi
        self.df_measure["eye_area_r"] = (self.measure_euclid_dist(43, 46) / 2) * ((self.measure_euclid_dist(44, 48) + self.measure_euclid_dist(45,47)) /2) * np.pi
        self.df_measure["eye_area"] = (self.df_measure["eye_area_l"] + self.df_measure["eye_area_r"])/2
        max_eye_area = self.df_measure["eye_area"].max()
        self.df_measure["eye_area_theshold"] = pd.DataFrame(threshold*np.arange(self.df_measure["frame"].max()/threshold))
        eye_area_mean = []
        for i in range(0,len(np.arange(self.df_measure["frame"].max()/threshold))):
            eye_area_mean.append(self.df_measure[self.df_measure["frame"].between(i,threshold*(i+1))]["eye_area"].mean())
        self.df_measure["eye_area_mean_over_"+str(threshold)+"_frame"] = pd.DataFrame(eye_area_mean)
        print(self.df_measure)

    def plot_measure(self, measure, axis_x = "frame"):
        discontinuities_frame  = self.find_discontinuities()
        video_fps = self.df_videos_infos[self.df_videos_infos["video_name"] == self.video_name]["fps"]
        #print(float(video_fps))
        if axis_x == "frame" :
            for index in discontinuities_frame:
                plt.plot(self.df_measure[self.df_measure[axis_x].between(index[0],index[1])][axis_x]/float(video_fps), self.df_measure[self.df_measure[axis_x].between(index[0],index[1])][measure])
        else :
            plt.plot(self.df_measure[axis_x], self.df_measure[measure])
        plt.xlabel("sec")
        plt.ylabel(measure)
        plt.show()

    def find_discontinuities(self):
        cmp = 0
        discontinuities_frame = [0]
        for index, row in self.df_measure.iterrows():
            if(row['frame'] != cmp) :
                discontinuities_frame.append(cmp-1)
                discontinuities_frame.append(row['frame'])
                cmp = row['frame']
            cmp = cmp + 1
        discontinuities_frame.append( cmp-1)
        result = zip(discontinuities_frame[::2], discontinuities_frame[1::2])
        return list(result)


ad = AnalyseData("data/data_out/DESFAM_Semaine 2-Vendredi_Go-NoGo_H69.csv")
#ad.measure_ear()
#ad.plot_measure("ear")
ad.measure_perclos(1,10)
ad.plot_measure("eye_area_mean_over_10_frame","eye_area_theshold")
