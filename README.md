# 🐱 CAT-FIGHT

I built this little project to finally answer a question that’s been on my mind while hanging out with my cat, Haitai:
If my cat were a fighting game character, what would his stats be??

This tool takes the idea and runs with it. Just upload a video of a cat (or multiple!), and it uses computer vision to identify each cat and create a unique Super Smash Bros.–style fighter profile.

You’ll get their attack power, defense, a special move, and even a signature catchphrase they’d shout before battle.

*Dog person? No worries — a new edition is coming soon!*

---

## How It Works 🛠️

*   **Backend:** A Python server using the **Flask** framework.
*   **Computer Vision:** I used **OpenCV** to handle the video and the **YOLOv8** model to find and isolate each cat in the video frames.
*   **AI Character Design:** The cropped portrait of each cat is sent to the **Claude 3.5 Sonnet API**, which acts as the game designer to create the stats and personality.
*   **Frontend:** The retro arcade interface is built with standard **HTML**, **CSS**, and **JavaScript**.

---


**➡️ [Try Cat-Fight Live Here](https://a05c-2601-640-8d01-5720-b4a1-7bb2-9838-3ef6.ngrok-free.app/)**

**Note:** This demo is hosted on my local machine via ngrok, so it will only be active when my computer is on :)


## Example 📸 




