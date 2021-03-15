# Name: Yili Liu    Student ID: 205376049

import zlib, os, sys

# hash, parents, and children for each commit (credits to project spec)
class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()

# find the .git directory by starting from the current directory (top level)
# and ascending to parent directories until found
def get_git_dir():
    dir = os.getcwd()
    while dir != '/':
        if os.path.exists('.git') == True:
            return dir
        os.chdir('../')
        dir = os.getcwd()
    sys.stderr.write("Not inside a Git repository\n")
    exit(1)

# returns the heads of all local branches (associated w commit hash)
def get_branches(dir):
    branches, commit_nodes = {}, {} # dictionaries storing branch heads and commit nodes
    m_hash = set() # hash maps
    dir = os.path.join(dir, ".git/refs/heads") # branch directory
    os.chdir(dir)
    for root, dirs, files in os.walk("."):
        for f in files:
            file = os.path.join(root, f)
            if os.path.isfile(file): # check that it is a valid file
                temp_hash = open(file, 'r').read().strip()
                if temp_hash not in branches:
                    branches[temp_hash] = []
                branches[temp_hash].append(file[2:]) # append branch name to branches
                m_hash.add(temp_hash)
    return branches, commit_nodes, m_hash
    
# build a commit graph through a depth first search
# taking leaf nodes and traveling down the branch, continually apending commits
def build_commit_graph(dir, commit_nodes, hash_set):
    root = set() # hash map of all root commits
    hash = sorted(hash_set) # sort our hash
    while len(hash) > 0:
        commit = hash.pop() # get last commit and pop it when done
        if commit not in commit_nodes:
            commit_nodes[commit] = CommitNode(commit)
            sub_dir = commit[:2]
            file = commit[2:]
            obj_dir = os.path.join(dir, ".git/objects", sub_dir, file)
            compressed = open(obj_dir, 'rb').read()
            decompressed = zlib.decompress(compressed).decode().splitlines()
            for line in decompressed:
                i = line.find('parent') # look for the parent node in the line
                if i != -1:
                    parent = line[i+6:].strip()
                    # add parents hash to commit_nodes
                    commit_nodes[commit].parents.add(parent)
                    if parent not in commit_nodes:
                        hash.append(parent)
            if len(commit_nodes[commit].parents) == 0: # new root commit
                root.add(commit)
    
    # add children to the parent in commit_nodes
    for n in commit_nodes:
        for parent in list(commit_nodes[n].parents):
            commit_nodes[parent].children.add(n)
            
    return commit_nodes, root
 
# generates topological ordering of commits in graph
# a total ordering of the commit nodes such that all the descendent commit nodes
# are strictly less than the ancestral commits, where nodes in root are
# the oldest ancestors.
def topo_order(commit_nodes, root):
    ordered = [] # sorted ordering of commits
    visited = set() # keep track of what has been visited
    for r in sorted(list(root)):
        stack = [r]
        while stack:
            visited.add(stack[-1])
            append_child = False
            # if child node is not visted, append it to the stack
            for child in sorted(list(commit_nodes[stack[-1]].children)):
                if child not in visited:
                    stack.append(child)
                    append_child = True
            if append_child == False: # only append to ordered if children not already there
                if stack[-1] not in ordered:
                    ordered.append(stack[-1])
                stack.pop()
    return ordered

# print the commit hashes from least to greatest
# If the next commit to be printed is not the parent of the current commit
# a “sticky end” is inserted followed by an empty line before printing the next commit
def print_commits(ordered, branches, commit_nodes):
    jumped = False
    for i in range(len(ordered)):
        commit_hash = ordered[i]
        if jumped:
            jumped = False
            sticky_hash = ' '.join(commit_nodes[commit_hash].children)
            print(f'={sticky_hash}')
        branch = sorted(branches[commit_hash]) if commit_hash in branches else []
        print(commit_hash + (' ' + ' '.join(branch) if branch else ''))
        if i + 1 < len(ordered) and ordered[i + 1] not in commit_nodes[commit_hash].parents:
            jumped = True
            sticky_hash = ' '.join(commit_nodes[commit_hash].parents)
            print(f'{sticky_hash}=\n')

# Call all above functions to do topological sort then print the result
def topo_order_commits():
    dir = get_git_dir()
    branches, commit_nodes, hash_set = get_branches(dir)
    commit_nodes, root = build_commit_graph(dir, commit_nodes, hash_set)
    ordered = topo_order(commit_nodes, root)
    print_commits(ordered, branches, commit_nodes)

if __name__ == '__main__':
    topo_order_commits()

