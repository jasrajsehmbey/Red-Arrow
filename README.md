# Red-Arrow
Detects Red Arrow and finds its angle with the verticle. Made by using Opencv in python.
Made this project by using:-
1. Detecting only red colour using a trackbar. Then used mask. (inRange and bitwaise_and)
2. When the red colour is detected, i used findcontour() to get the boundary of detected red colour.
3. Used HoughLinesP() to detect only straight lines.
4. When a straight line is detected the program runs forward and then i use approxPolyDP() to approximate the end points of detected object 
5. Then i gave a condition if the edges are equal to 7 and the area of it is more than a perticular small value then it lables it as a red arrow
6. I used minAreaRect() to get the angle of the arrow. this gives us a rotating rectangle around the arrow and forms a tuple in which the 2nd position is its angle.
