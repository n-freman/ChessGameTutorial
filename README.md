# Chess Making video tutorial completion   
I strated this tutorial on 21.01.2022.<br>
Hope to finish it in two weeks.<br>
22.01.22 12:28 Finished 01/16 tutorial.<br>
22.01.22 13:42 Finished 02/16 tutorial.<br>
23.01.22 09:44 Finished 03/16 tutorial.<br>
23.01.22 18:35 Finished 04/16 tutorial.<br>
24.01.22 11:52 Finished 05/16 tutorial.<br>
24.01.22 14:22 Finished 06/16 tutorial.<br>
25.01.22 10:18 Finished 07/16 tutorial.<br>
25.01.22 12:00 Finished 08/16 tutorial.<br>
26.01.22 14:45 Finished 09/16 tutorial.<br>
27.01.22 10:50 Finished 10/16 tutorial.

---

## About my own changes to the project
I am also going to add few lines to resize images of pieces.<br>
I saw that in tutorial author uses pictures of prepared size.<br>
Added some changes to the variable names, because author used not pythonic naming convention<br>
(he actually says that he is the JAVA guy).<br>
Also added my own pieces and colors for game board.<br>
Added functionality for making pieces smaller than the squares.<br>
Rewrote some functions ('undo_move', get_piece_move for each piece) on my own way.<br>
Created selected and movable square highlighting function.s

---

## Notes
Found out that not only the pieces are redrawed, but the whole gameboard is.

---

## HOW TO RUN THE GAME
First you need to install any version of python3 from python.org<br>
Second you should install pip.<br>
If you are on Windows it comes with python3.<br>
if you are on Linux you just run the next command:
```
sudo apt update
sudo apt install pip
```
And then on both Windows and Linux you need to install pygame:
```
pip install pygame
```
Then just get the copy of the project and run it:
```
git clone https://github.com/tiberius-kirk/ChessGameTutorial.git
cd ChessGameTutorial
python main.py
```