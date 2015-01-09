#! /bin/bash

# Runs org.ggp.base.apps.utilities.GameServerRunner, a command-line only server. 
# Just a small layer of script.  Less of something that needs to be a script, 
# more just a way to write down the fact that you need to change the classpath
# and it has to be pretty specific.  

lib_st="/Users/gsj601/git/ggp-hardware.git/lib/"
cp_var="/Users/gsj601/git/ggp-hardware.git/build/classes/main/"
cp_var="${cp_var}:${lib_st}Batik/*"
cp_var="${cp_var}:${lib_st}Clojure/*"
cp_var="${cp_var}:${lib_st}FlyingSaucer/*"
cp_var="${cp_var}:${lib_st}Guava/*"
cp_var="${cp_var}:${lib_st}Htmlparser/*"
cp_var="${cp_var}:${lib_st}JFreeChart/*"
cp_var="${cp_var}:${lib_st}JGoodiesForms/*"
cp_var="${cp_var}:${lib_st}JUnit/*"
cp_var="${cp_var}:${lib_st}Jython/*"
cp_var="${cp_var}:${lib_st}javassist/*"
cp_var="${cp_var}:${lib_st}reflection/*"

# Good defaults for the arguments to this script:
# testing ticTacToe 60 30 localhost 9147 First localhost 9148 Second
# Note that you'll need to have two players running, with those ports. 
# The easiest way to get two players running with those ports is to run 
# ./gradlew player
# and then create two new players.  914{7,8} are the default ports of the first
# two created players. 

echo $cp_var

java -cp $cp_var org/ggp/base/apps/utilities/GameServerRunner $@

