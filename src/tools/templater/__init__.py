import sys, os, os.path

this_abs = os.path.join(os.getcwd(), __file__)
src_dir = os.path.abspath( os.path.join(this_abs, "..", "..") )
sys.path.append( src_dir )


#print sys.path