from classes import expression,node

def popnext(stream, token):
	if stream[0:len(token)] == list(token):
		del stream[0:len(token)]
		return True
	return False

def parse_binary(stream, operator, nextfn):
	es = [nextfn(stream)]
	while popnext(stream, operator):
		es.append(nextfn(stream))
	return '('+'{}'.format(operator).join(es) + ')' if len(es) > 1 else es[0]

def parse_ors(stream):
	return parse_binary(stream, '+', parse_ands)

def parse_ands(stream):
	return parse_binary(stream, '.', parse_unary)

def parse_unary(stream):
	if popnext(stream, '!'):
		return '!{}'.format(parse_unary(stream))
	return parse_primary(stream)

def parse_primary(stream):
	if popnext(stream, '('):
		e = parse_ors(stream)
		popnext(stream, ')')
		return e
	return stream.pop(0)

def parse(expression):
	return parse_ors(list(expression.replace(' ', '')))

def create_tree(exp):
	stack=["("]
	exp=exp[1:]
	root=node('')
	while stack and exp:
		curr=exp[0]
		exp=exp[1:]
		if(curr.isalpha()):
			op=stack[-1]
			if(op=="!" and root.left==None):
				root.left=node("!",node(curr))
			elif(root.left==None):
				root.left=node(curr)
			elif(op in "+."):
				stack.pop()
				root.right=node(curr)
				temp=root
				root.value=op
				root=node('')
				root.left=temp
			elif(op=="!"):
				stack.pop()
				root.value=stack.pop()
				root.right=node("!",node(curr))
				temp=root
				root=node('')
				root.left=temp
		elif curr in ".+!":
			stack.append(curr)
		elif(curr=="("):
			op=stack[-1]
			count,ind=1,0
			for i in range(0,len(exp)):
				if(exp[i]=="("):
					count+=1
				elif(exp[i]==")"):
					count-=1
					if(count==0):
						ind=i
						break
			new="("+exp[0:ind+1]
			exp=exp[ind+1:]
			if(op=="!" and root.left==None):
				root.left=node("!",create_tree(new))
			elif(root.left==None):
				root.left=create_tree(new)
			elif(op in "+-"):
				root.right=create_tree(new)
				temp=root
				root.value=stack.pop()
				root=node('')
				root.left=temp
			elif(op=="!"):
				stack.pop()
				root.right=node("!",create_tree(new))
				temp=root
				root.value=stack.pop()
				root=node('')
				root.left=temp
		elif(curr==")"):
			stack.pop()
	if(root.value==''):
		return root.left
	return root

def create_simfile(exp,filename):
	exp="(%s)"%parse("(%s)"%exp)
	root=create_tree(exp)
	if len(exp)==3:
		print("\nError!")
		return -1
	# root.print()
	sim_file=open(filename,"w")
	sim_file.write("| units: 100 tech: scmos format: MIT\n\n")
	root.sim_file_from_tree(sim_file)
	sim_file.write("| sim file generated using sim_creater.py\n")
	sim_file.write("| boolean expression is %s"%exp[1:-1])
	sim_file.close()
	print("\n%s created successfully"%filename)
	print("\nboolean expression is %s"%exp[1:-1])