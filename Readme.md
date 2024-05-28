# PLush
- PLush is a language made for people that are now starting to learn programming
- PLush is a language that is easy to learn and understand
- PLush is not complex. Its only possible to make simple programs with it. But it's enough to understand simple programming concepts
- PLush is written in python, and it's compiled to llvm
- Plush also has an interpreter that can be used to run the code without compiling it

# How to use PLush
- To start using PLush it is recommend for you to have docker installed. If you don't have docker installed you can install it by following the instructions on the official docker website
- After you have docker installed you can run the following commands to start using PLush
```
cd code/
bash instal.sh 
```
- This command will create the image of plush and start the container. After that, you will be inside the container.
- One important aspect of this container is that, the past compiler is mounted, soo if you want to write new code you can write it in your local machine and then run the code inside the container. Just be sure to store the file in the code/compiler folder
- Or you can use vim to write the code inside the container. For that you have to download yourself the vim package. You can do that by running the following command
```
apt-get update
apt-get install vim
```
- But there are some test codes in the paste tests/program_tests that you can use to test the compiler. 
- To run the compiler use the following command
```
bash plush.sh path_to_the_file <flags>
```
- The PLush supports some flags.

| Flag | Description |
|------|-------------|
| -json   | This will write in the paste **generated_files** the json of the ast after the type checker |
| -i    | Instead of using the compiler, it will use the **interpreter** |
| -args | This will pass the arguments to the program. Use this flag as the last one, if not the others will be considered as another string to argv. |