import tkinter as tk
from tkinter import messagebox, font as tkfont
from threading import Thread
import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
import math
import random
import time

# Placeholder SnakeGame class
class SnakeGame:
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        detector = HandDetector(detectionCon=0.8, maxHands=1)

        class SnakeGameClass:
            def __init__(self, pathFood):
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point

                self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
                self.hFood, self.wFood, _ = self.imgFood.shape
                self.foodPoint = 0, 0
                self.randomFoodLocation()

                self.score = 0
                self.gameOver = False

            def randomFoodLocation(self):
                self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

            def update(self, imgMain, currentHead):

                if self.gameOver:
                    cvzone.putTextRect(imgMain, "Game Over", [300, 400],
                                       scale=7, thickness=5, offset=20)
                    cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550],
                                       scale=7, thickness=5, offset=20)
                else:
                    px, py = self.previousHead
                    cx, cy = currentHead

                    self.points.append([cx, cy])
                    distance = math.hypot(cx - px, cy - py)
                    self.lengths.append(distance)
                    self.currentLength += distance
                    self.previousHead = cx, cy

                    # Length Reduction
                    if self.currentLength > self.allowedLength:
                        for i, length in enumerate(self.lengths):
                            self.currentLength -= length
                            self.lengths.pop(i)
                            self.points.pop(i)
                            if self.currentLength < self.allowedLength:
                                break

                    # Check if snake ate the Food
                    rx, ry = self.foodPoint
                    if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                            ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                        self.randomFoodLocation()
                        self.allowedLength += 50
                        self.score += 1
                        print(self.score)

                    # Draw Snake
                    if self.points:
                        for i, point in enumerate(self.points):
                            if i != 0:
                                cv2.line(imgMain, self.points[i - 1], self.points[i], (136, 91, 118), 25)
                        cv2.circle(imgMain, self.points[-1], 30, (152, 0, 255), cv2.FILLED)

                    # Draw Food
                    imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                                (rx - self.wFood // 2, ry - self.hFood // 2))

                    cvzone.putTextRect(imgMain, f'SCORE CARD: {self.score}', [50, 80],
                                       scale=3, thickness=3, offset=10)

                    # Check for Collision
                    pts = np.array(self.points[:-2], np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
                    minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

                    if -1 <= minDist <= 1:
                        print("Hit")
                        self.gameOver = False
                        self.points = []  # all points of the snake
                        self.lengths = []  # distance between each point
                        self.currentLength = 0  # total length of the snake
                        self.allowedLength = 150  # total allowed Length
                        self.previousHead = 0, 0  # previous head point
                        self.randomFoodLocation()

                return imgMain

        game = SnakeGameClass('EGG.png')

        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=True)

            if hands:
                lmList = hands[0]['lmList']
                pointIndex = lmList[8][0:2]
                img = game.update(img, pointIndex)
            cv2.imshow("Image", img)
            key = cv2.waitKey(1)
            if key == ord('R'):  # for quit the game
                game.gameOver = True
                break

        messagebox.showinfo("Game Info", "Snake Game started. Implement game logic.")

# Placeholder RockPaperScissorsGame class
class RockPaperScissorsGame:
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        detector = HandDetector(maxHands=1)

        timer = 0
        stateResult = False
        startGame = False
        scores = [0, 0]  # [AI, Player]
        initialTime = 0  # Declare initialTime here to ensure its scope is throughout the script

        while True:
            imgBG = cv2.imread("Resources/BG.png")
            success, img = cap.read()

            imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
            imgScaled = imgScaled[:, 80:480]

            # Find Hands
            hands, img = detector.findHands(imgScaled)  # with draw

            if startGame:
                if stateResult is False:
                    timer = time.time() - initialTime  # Update the timer based on the current time minus the initial time
                    cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_TRIPLEX, 5, (255, 0, 255), 8)

                    if timer > 3:
                        stateResult = True
                        # Reset the timer here for the next round
                        if hands:
                            playerMove = None
                            hand = hands[0]
                            fingers = detector.fingersUp(hand)
                            if fingers == [0, 0, 0, 0, 0]:
                                playerMove = 1
                            if fingers == [1, 1, 1, 1, 1]:
                                playerMove = 2
                            if fingers == [0, 1, 1, 0, 0]:
                                playerMove = 3

                            randomNumber = random.randint(1, 3)  # this is for random nummber generation starts here
                            imgAI = cv2.imread(f"Resources/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                            # Player Wins
                            if (playerMove == 1 and randomNumber == 3) or \
                                    (playerMove == 2 and randomNumber == 1) or \
                                    (playerMove == 3 and randomNumber == 2):
                                scores[1] += 1

                            # AI Wins
                            if (playerMove == 3 and randomNumber == 1) or \
                                    (playerMove == 1 and randomNumber == 2) or \
                                    (playerMove == 2 and randomNumber == 3):
                                scores[0] += 1

            imgBG[234:654, 795:1195] = imgScaled

            if stateResult:
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

            cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 6)
            cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 6)

            cv2.imshow("BG", imgBG)

            key = cv2.waitKey(1)
            if key == ord('S'):
                startGame = True
                initialTime = time.time()  # Set the initial time to the current time when the game starts
                stateResult = False  # Reset the game state for the new round
            if key == ord('R'):
                break

    messagebox.showinfo("Gesture- Tech Innovators", "Choose any game to play")

def run_game(game_class):
    try:
        game = game_class()
        game.run()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def start_snake_game():
    Thread(target=lambda: run_game(SnakeGame), daemon=True).start()

def start_rps_game():
    Thread(target=lambda: run_game(RockPaperScissorsGame), daemon=True).start()

def main_app():
    root = tk.Tk()
    root.title("Interactive Gesture Based Gaming Platform")
    root.geometry("1920x1080")  # Set the window size
    root.configure(bg="#282828")  # Set background color

    # Styling for the buttons and label
    btn_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
    label_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
    btn_color = "#00CC66"
    text_color = "#FFFFFF"

    # Header label
    header_label = tk.Label(root, text="GESTURE TECH INNOVATORS GAMING PLATFORM", bg="#282828", fg=text_color, font=label_font)
    header_label.pack(pady=10)

    # Snake Game Button
    btn_snake_game = tk.Button(root, text="Start Snake Game", bg=btn_color, fg=text_color, font=btn_font, command=start_snake_game)
    btn_snake_game.pack(pady=10, padx=20, fill=tk.X)

    # Rock-Paper-Scissors Game Button
    btn_rps_game = tk.Button(root, text="Start Rock-Paper-Scissors Game", bg=btn_color, fg=text_color, font=btn_font, command=start_rps_game)
    btn_rps_game.pack(pady=10, padx=20, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main_app()
