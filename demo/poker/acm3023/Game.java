
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;
import java.lang.Integer;

public class Game {
    
    private Player p;
    private Deck cards;
    private ArrayList<Card> hand;
    // you'll probably need some more here
    
    
    public Game(String[] testHand){
        // This constructor is to help test your code
        // use the contents of testHand to
        // make a hand for the player
        // use the following encoding for cards
        // c = clubs
        // d = diamonds
        // h = hearts
        // s = spades
        // 1-13 correspond to ace - king
        // example: s1 = ace of spades
        // example: testhand = {s1, s13, s12, s11, s10} = royal flush
        p= new Player();
        cards= new Deck();
        cards.shuffle();
        makeHand(testHand);
        // hand takes the value of a copy 
        // of the player's hand
        hand=new ArrayList<Card>(p.getHand());

        System.out.println(checkHand(hand));
    }
        
        
    
    
    public Game(){
        // This constructor is to actually play a normal game
        p= new Player();
        cards= new Deck();
        cards.shuffle();
        // the loop adds 5 dealt cards 
        // to the player's hand
        for(int i=1; i<6; i++){
            p.addCard(cards.deal());
        } 
        // hand takes the value of a copy 
        // of the player's hand
        hand= new ArrayList<Card>(p.getHand());
    }
    
    public void play(){
        // this method should play the game 
        Scanner s= new Scanner(System.in);
        print("Poker Game");
        print("These are the cards dealt:");
        // this loop will print the cards from the hand
        for (Card element: hand){
            print(""+element);  // the card element is casted to a string 
                                // using the toString method in Card
        }
        
        print("How many cards do you want to reject? 0-5");
        int reject=s.nextInt(); // this is the number of cards to be rejected
        if (reject>0){
            for(int i=0; i<reject; i++){
                // the user is asked to say 
                // what card is to be rejected
                // this is asked the as many times 
                // as the number of cards the user 
                // wants to reject
                print("What card do you want to reject? 1, 2, 3, 4, or 5");
                int rejected= s.nextInt();
                // remove the card that the user wants to reject 
                // from the hand in the player class
                p.removeCard(hand.get(rejected-1));
                // deal a card to that hand
                p.addCard(cards.deal());
            }
        }
        // the variable hand takes the value of a copy
        // of the player's hand
        hand=new ArrayList<Card>(p.getHand());
        // the cards are printed again
        print("This is your new hand");
        for (Card element: hand){
            print(""+element);
        }
        // The hand is then evaluated
        String result=checkHand(hand);
        print("Your hand has a "+result);    
    }
    
    public String checkHand(ArrayList<Card> hand){
        // this method should take an ArrayList of cards
        // as input and then determine what evaluates to and
        // return that as a String
        hand=sortHand(hand);   // the hand is first sorted
        
        // the method evaluates if the hand 
        // has any of the possible hands 
        // strating from the best possible 
        // (royal flush)
        // if the hand is none of the hands it is a no pair
        
        if (royalFlush(hand)==1){
            return "Royal Flush";
        }
        else if (straightFlush(hand)==1){
            return "Straight Flush";
        }
        else if (four(hand)==1){
            return "Four of a kind";
        }
        else if(fullHouse(hand)==1){
            return "Three of a kind";
        }
        else if (flush(hand)==1){
            return "Flush";
        }
        else if (straight(hand)==1){
            return "Straight";  
        }
        else if (three(hand)==1){
            return "Three of a kind";
        }
        else if (twoPairs(hand)==1){
            return "Two Pairs";
        }
        else if (pair(hand)==1){
            return "One pair";
        }
        else{
            return "No Pair";
        }
    }
    

    public int pair(ArrayList<Card> hand){
        //returns the number of pairs in the hand
        //three of a kind count as one pair
        Card temp;
        int i=1;
        int numberPairs=0;        
        while (i<hand.size()){
            temp=hand.get(i-1);
            if (temp.sameValue(hand.get(i))){
                i++;
                numberPairs++;
            }
            i++;
        }
        return numberPairs;
    }
    
    public int twoPairs(ArrayList<Card> hand){
        // assumes the hand has five cards
        // returns 1 if the hand has two pairs and 0 otherwise
        if(pair(hand)==2){
            return 1;   
        }
        else{
            return 0;
        }
    }
    
    public int three(ArrayList<Card> hand){
        //assumes the hand has five cards
        if (pair(hand)==0){
            // to have three of a kind a hand has to have a pair
            return 0;    
        }
        else if( hand.get(0).sameValue(hand.get(2)) 
                || hand.get(1).sameValue(hand.get(3)) 
                    || hand.get(2).sameValue(hand.get(4))){
                return 1;
            }
        else {
            return 0;
        }
    }
    
    public int straight(ArrayList<Card> hand){
        // returns 1 if the hand has a straight and 0 otherwise
        Card one = hand.get(0);
        Card five = hand.get(4);
        Card two = hand.get(1);
        if (pair(hand) > 0){
            // the hand can't have a pair
            return 0;
        }
        else if(five.difValue(one)==4){
            // the difference between the value of
            // the first and last card has to be 4
            return 1;
        }
        else if(one.getValue()==1 && five.getValue()==13 
                && two.getValue()==10){
            // this accounts for the possibility
            // of the ace counting after a king
            return 1;
        }
        else{
            return 0;
        }       
    }
    
    public int flush(ArrayList<Card> hand){
        // returns 1 if the hand has a flush 
        // 0 otherwise
        if(pair(hand)>0){
            // to have a flush the hand can't have a pair
            // because a pair is always two cards of different suits
            return 0;
        }
        else{      
            int i=1;
            for(Card element: hand){
                if (! element.sameSuit(hand.get(i))){
                    // the moment two consecutive cards 
                    // don't have the same suit
                    // the method returns 0
                    return 0;
                }
                if(i<hand.size()-1){
                    // in the last evaluation of the for loop 
                    // the last element of the hand will be 
                    //compared with itself
                    i++;
                }    
            }
            return 1;
        }     
    }
    
    public int fullHouse(ArrayList<Card> hand){
        // returns 1 if the hand is a Full House
        // 0 otherwise
        if (pair(hand)==2 && three(hand)==1 && four(hand)==0){
            // a full house has one pair one three of a kind and 0 
            // four of a kind
            return 1;
        }
        else{
            return 0;
        }    
    }    
    
    public int four(ArrayList<Card> hand){
        // returns 1 if the hand has 4 cards with the same value
        if (pair(hand)==2 && three(hand)==1){
            if(hand.get(0).sameValue(hand.get(3)) 
                        || hand.get(1).sameValue(hand.get(4))){ //mandy fix 5-4
                // this distinguishes from a full house
                return 1;
            }
        }
        return 0;            
    }    
    
    public int straightFlush(ArrayList<Card> hand){
        // returns 1 if the hand has a straight flush
        if (flush(hand)==1 && straight(hand)==1){
            return 1;
        }
        else{
            return 0;
        }
    }
    
    public int royalFlush(ArrayList<Card> hand){
        // returns 1 if the hand has a royal flush
        if (straightFlush(hand)==1 && hand.get(0).getValue()==1){
            return 1;
        }
        else{
            return 0;
        }
    }
        
    
    public void makeHand(String[] testHand){
        // this method makes a hand from a array of strings
        Card card; 
        // in the strings the suit corresponds to the first character
        char suitChar;
        int suit;
        int value=1;
        String valueString;
        for(int i=0; i<5; i++){
            suitChar=testHand[i].charAt(0);
            valueString= testHand[i].substring(1);
            // the value of the integer is the last part of the string 
            // either one or two characters that from an integer form 
            // 1 to 13
            value= Integer.parseInt(valueString);
            if (suitChar=='c'){
                suit=1;
            }
            else if (suitChar=='d'){
                suit=2;
            }
            else if (suitChar=='h'){
                suit=3;
            }
            else{
                suit=4;
            }
            card= new Card(suit, value);
            p.addCard(card);
        }
        
    }
        
    public ArrayList<Card> sortHand(ArrayList<Card> hand){
        // this method returns a sorted hand 
        Collections.sort(hand);
        return hand;
    }
    
    public void print(String s){
        // this method is a shortcut to print a string
        System.out.println(s);
    }
}



