change names in the names.csv file

format:
NAMES
name1
name2
name3
....

While adding lots of names into the same certificate, seperate them with a comma (',')

the results will be in the 'results' folder.

prequisites: python, open cv(cv2), numpy, pandas

Steps:
1. Base certificate is loaded in '1st.png'
2. The part where the name is supposed to go is painted the colour, #FF00FF (RGB)
3. Put names in the names.csv file
4. Get results

(More automation and a GUI will be added after the base functionality is properly working)

To be added:
1. Auto sizescaling of text if it doesn't fit
