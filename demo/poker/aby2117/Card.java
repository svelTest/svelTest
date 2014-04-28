

public class Card implements Comparable<Card> {
    private int suit; // use integers 1-4 to encode the suit
    private int value; // use integers 1013 to encode the value
   
    
    public Card(int s, int v){
        //make a card with suit s and value v
        suit = s;
        value= v;
            
    }
    
    public int compareTo(Card c){
        // use this method to compare cards so they 
        // may be easily sorted
        // the method returns 0 if the cards are the same
        // a positive int if the implicit variable card is greater
        // a negative int if the implicit variable card is smaller
        // the ace of clubs is considered to 
                //be the smallest card of the deck
        // the king of spades is the greatest card of the deck
        
        //first compare the values of the cards
        int answer=this.getValue()- c.getValue();
        
        //if the cards have the same values we compare them by suit
        if(answer==0){
            answer=this.getSuit()- c.getSuit();
        }
        return answer;

    }
    
    public int getSuit() {
        return suit;
    }

    public int getValue() {
        return value;
 
    }
    
    
    public boolean sameValue(Card c){
        // this method returns true if the cards have the same value
        // and false otherwise
        return this.getValue()==c.getValue();
    }
    
    
    public int difValue(Card c){
        // this method returns the difference 
        // between the values of the two cards
        return this.getValue()-c.getValue();
    }
    
    public boolean sameSuit(Card c){
        //this method returns true if the cards have the same suit
        // false otherwise
        return this.getSuit()==c.getSuit();
    }

    public String toString(){
        // use this method to easily print a Card object
        // the order of the cards by suit is the reverse alphabetical order
        
        String nameSuit="0";
        String nameValue = "0";
        
        //the suits are 1-c:clubs, 2-d:diamonds, 3-h:hearts, 4-s:spades
        if(suit==1){
            nameSuit="clubs";
        }
        else if(suit==2){
            nameSuit="diamonds";
        }
        else if(suit==3){
            nameSuit="hearts";
        }
        else{
            nameSuit="spades";
        }
        
        //assign the string to the value of the card
        if(value>1 && value<11){
            nameValue=""+value;
        }
        
        else if(value==1){
            nameValue="Ace";
        }
        
        else if(value==11){
            nameValue="Jack";
        }
        
        else if(value==12){
            nameValue="Queen";
        }
        
        else if(value==13){
            nameValue="King";
        }
        
        //a card object is printed in the form of 
        //the card value followed by the suit
        
        String nameCard=nameValue+" of "+nameSuit;
        return nameCard;
    }
}
