package dk.itu.mario.engine.level;

import java.util.Random;
import java.util.*;

//Make any new member variables and functions you deem necessary.
//Make new constructors if necessary
//You must implement mutate() and crossover()


public class MyDNA extends DNA
{
	
	public int numGenes = 0; //number of genes
	//public String levelString = "";

	// Return a new DNA that differs from this one in a small way.
	// Do not change this DNA by side effect; copy it, change the copy, and return the copy.
	public MyDNA mutate ()
	{
		MyDNA copy = new MyDNA();
		//YOUR CODE GOES BELOW HERE
		Random rand = new Random();
		int randDNAIndex = rand.nextInt(this.getLength());
		//int randDNAIndex2 = rand.nextInt(this.getLength());
		//int randDNAIndex3 = rand.nextInt(this.getLength());
		char[] profiles = new char[] {'j', 'c', 'h', 't', 's', 'a', 'g', 'q', 'n'};
		int randProfIndex = rand.nextInt(profiles.length);
		//int randProfIndex2 = rand.nextInt(profiles.length);
		//int randProfIndex3 = rand.nextInt(profiles.length);
		char[] copyChar = this.getChromosome().toCharArray();
		copyChar[randDNAIndex] = profiles[randProfIndex];
		//copyChar[randDNAIndex2] = profiles[randProfIndex2];
		//copyChar[randDNAIndex3] = profiles[randProfIndex3];
		copy.setChromosome(String.valueOf(copyChar));
		//YOUR CODE GOES ABOVE HERE
		return copy;
	}
	
	// Do not change this DNA by side effect
	public ArrayList<MyDNA> crossover (MyDNA mate)
	{
		ArrayList<MyDNA> offspring = new ArrayList<MyDNA>();
		//YOUR CODE GOES BELOW HERE
		MyDNA offspring1 = new MyDNA();
		MyDNA offspring2 = new MyDNA();
		char[] charArr1 = new char[this.getLength()];
		char[] charArr2 = new char[this.getLength()];
		Random rand = new Random();
		int randMod = rand.nextInt(2);
		//int halfPoint = this.getLength()/2;
		for (int i = 0; i < this.getLength(); i++) {
			if (randMod == 0) {
				charArr1[i] = this.getChromosome().charAt(i);
				charArr2[i] = mate.getChromosome().charAt(i);
			} else {
				charArr1[i] = mate.getChromosome().charAt(i);
				charArr2[i] = this.getChromosome().charAt(i);
			}
			randMod = rand.nextInt(2);
		}
		offspring1.setChromosome(String.valueOf(charArr1));
		offspring2.setChromosome(String.valueOf(charArr2));
		offspring.add(offspring1);
		offspring.add(offspring2);
		//YOUR CODE GOES ABOVE HERE
		return offspring;
	}
	
	// Optional, modify this function if you use a means of calculating fitness other than using the fitness member variable.
	// Return 0 if this object has the same fitness as other.
	// Return -1 if this object has lower fitness than other.
	// Return +1 if this objet has greater fitness than other.
	public int compareTo(MyDNA other)
	{
		int result = super.compareTo(other);
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return result;
	}
	
	
	// For debugging purposes (optional)
	public String toString ()
	{
		String s = super.toString();
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return s;
	}
	
	public void setNumGenes (int n)
	{
		this.numGenes = n;
	}

}

