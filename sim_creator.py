from functions import create_simfile

if __name__ == "__main__":
	print("Please use + for or, . for and, ! for not and () for braces only. Also please use single character variables\n")
	exp=input("Enter expression : ")
	filename=input("Enter filename : ")
	create_simfile(exp,filename)
	print("\n%s created successfully"%filename)