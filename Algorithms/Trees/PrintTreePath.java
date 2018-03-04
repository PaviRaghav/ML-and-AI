package Algorithms;

import Implementation.*;
import java.util.*;

public class PrintTreePath {
	public static void printPaths(BinaryTreeNode root, int[] path, int pathLen) {
		if (root == null)
			return;
		path[pathLen] = root.getData();
		pathLen++;
		if (root.getLeft() == null && root.getRight() == null)
			printArray(path, pathLen);
		else {
			printPaths(root.getLeft(), path, pathLen);
			printPaths(root.getRight(), path, pathLen);
		}
	}

	private static void printArray(int[] ints, int len) {
		for (int i = 0; i < len; i++)
			System.out.print(ints[i] + " ");
		System.out.println();
	}
	
	public void roottoleaf(BinaryTreeNode root, Deque<BinaryTreeNode> q) {
		if(root!=null) q.addFirst(root);
		if(root.left==null && root.right==null)
			q = print_nodes(q);
		else {
			if(root.left!=null) 
				roottoleaf(root.left,q);
			if(root.right!=null) 
				roottoleaf(root.right,q);
		}
		if(!q.isEmpty()) q.removeFirst();
	}
	private Deque<BinaryTreeNode> print_nodes(Deque<BinaryTreeNode> q){
		BinaryTreeNode temp = q.peekLast();
		do {
			System.out.print(q.peekLast().data + " ");
			q.addFirst(q.removeLast());
		} while(q.peekLast()!=temp);
		System.out.println();
		return q;
	}
	
	public static void main(String[] args) {
		BinaryTreeNode root = new BinaryTreeNode(1);
		root.left = new BinaryTreeNode(2);
		root.right = new BinaryTreeNode(3);
		root.left.left = new BinaryTreeNode(4);
		root.left.right = new BinaryTreeNode(5);
		root.left.right.left = new BinaryTreeNode(6);
		root.left.right.left.left = new BinaryTreeNode(7);
		PrintTreePath obj = new PrintTreePath();
		Deque<BinaryTreeNode> q = new LinkedList<BinaryTreeNode>();
		obj.roottoleaf(root, q);
	}
}
