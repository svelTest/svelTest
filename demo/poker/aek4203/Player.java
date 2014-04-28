
import java.util.ArrayList;

public class Player {
    private ArrayList<Card> hand; // the player's cards
    private int numberOfCards;
        
    public Player(){        
        // create a player here
        numberOfCards=0;
        hand= new ArrayList<Card>();
    }

    public void addCard(Card c){
        // add the card c to the player's hand
        hand.add(c);
        numberOfCards++;
    }

    public void removeCard(Card c){
        // remove the card c from the player's hand
        // if the number of cards is greater than 0
        if (numberOfCards>0){
            hand.remove(c);
            numberOfCards--;
        }
    }
    
    public ArrayList<Card> getHand(){
        // returns the ArrayList of cards corresponding 
        // to the players hand
        return hand;
    }
        
}
