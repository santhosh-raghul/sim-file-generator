class expression:

	def __init__(self,operator,operand_1,operand_2=''):
		self.operand_1=operand_1
		self.operand_2=operand_2
		self.operator=operator

	def __str__(self):
		return self.operand_1+self.operator+self.operand_2

	def create_sim(self,out):
		if(self.operator=='!'):
			return "p %s vdd %s 2 4\nn %s gnd %s 2 4\n\n"%(self.operand_1,out,self.operand_1,out)
		elif(self.operator=='+'):
			inter=self.operand_1+"_nor_"+self.operand_2+"_int"
			p1="p %s %s %s 2 4\n"%(self.operand_1,"vdd",inter)
			p2="p %s %s %s 2 4\n"%(self.operand_2,inter,out)
			n1="n %s %s %s 2 4\n"%(self.operand_1,out,"gnd")
			n2="n %s %s %s 2 4\n\n"%(self.operand_2,out,"gnd")
			return p1+p2+n1+n2
		elif(self.operator=='.'):
			inter=self.operand_1+"_nand_"+self.operand_2+"_int"
			p1="p %s %s %s 2 4\n"%(self.operand_1,"vdd",out)
			p2="p %s %s %s 2 4\n"%(self.operand_2,"vdd",out)
			n1="n %s %s %s 2 4\n"%(self.operand_1,out,inter)
			n2="n %s %s %s 2 4\n\n"%(self.operand_2,inter,"gnd")
			return p1+p2+n1+n2

class node:
	
	def __init__(self,value,left=None,right=None):
		self.value=value
		self.left=left
		self.right=right

	def print(self,l=0):
		if(self.right!=None):
			self.right.print(l+1)      
		print()
		print("   "*l,end="")
		print(self.value)
		if(self.left!=None):
			self.left.print(l+1) 

	def sim_file_from_tree(self,sim_file,id=0,invert=1):

		if(self.value not in "+.!"):
			return self.value

		out="out_%s"%id
		if(self.value=="!"):
			if(self.left.left==None):
				if(id==0):
					out="out"
				exp=expression("!",self.left.value)
				sim_file.write(exp.create_sim(out))
				return out
			else:
				if(id!=0):
					id+=1
				left_out=self.left.sim_file_from_tree(sim_file,id,0)
				return left_out
		else:
			left_out=self.left.sim_file_from_tree(sim_file,id+1)
			right_out=self.right.sim_file_from_tree(sim_file,id+2)
			exp=expression(self.value,left_out,right_out)
			if(out=="out_0" and not invert):
				out="out"
			sim_file.write(exp.create_sim(out))
			if(invert):
				exp=expression("!",out)
				if(out=="out_0"):
					out="out"
				else:
					out=out+"_o"
				sim_file.write(exp.create_sim(out))
			return out
