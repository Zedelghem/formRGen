# formRGen
## FormR Likert-Scale Survey Generator – For rapid preparation of norming surveys using formr.org

A tiny script to rapidly create formR-compatible Excel files for the purpose of large-scale norming studies utilizing a simple Likert scale.

To install the prerequisites run ```pip3 install --user XlsxWriter```.

To generate a file:
1. Input your words or statements into a text file, separated with new lines. By default, it should be called ```words.txt``` and located in the same folder as the scripts.
2. Adjust the ```config``` file to change the labels, pagination, output filename and path, etc.
3. Run ```formRGen.sh```.

Take a look at the config file for more information on what can be tinkered with.

The Excel file can be uploaded to formR.org straight away or appended with more questions – like the demographic section – manually.