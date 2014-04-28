
public class Deck {
    private Card[] theDeck;
    private int top; // the index of the top of the deck
    
    public Deck(){
        // make a 52 card deck here
        // the deck has the cards ordered
        // the top of the deck is the first card
        
        theDeck= new Card[52];
        int numberOfCards = 0;
        Card card;
        
        // add each card to the deck
        for (int s=1; s<5; s++){
            for (int v=1; v<14; v++){
                card= new Card(s, v);
                theDeck[numberOfCards]= card;
                numberOfCards++;
            }
        }
        top=0;
    }
    
    public void shuffle(){
        // shuffle the deck here
        Card temp;
        for (int i=1; i<1000; i++){
            int r = (int)(Math.random()*52);
            // switch the first card of the deck
            // with the card in the index randomly chosen
            temp=theDeck[0];
            theDeck[0]=theDeck[r];
            theDeck[r]=temp;    
        }
    }
    
    public Card deal(){
        // deal the top card in the deck
        // if the value of top is greater than 
        // the index of the last card of the deck
        // then the card dealt is a special card with 0 value and 0 suit
        if (top>51){
            top=0;
            return new Card(0,0);
        }
        else{
            top++;
            return theDeck[top-1];
        }
        
    }

}
