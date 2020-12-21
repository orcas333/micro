package main

func main() {
	// var card string = "Ace of Spades"
	// card = "Five of Diamonds"
	// card := newCard()
	// fmt.Println(card)

	// cards := deck{"Ace of Diamond", newCard()}
	// cards = append(cards, "Six of Spades")

	// cards := newDeck()

	// hand, remainingCards := deal(cards, 5)

	// hand.print()
	// remainingCards.print()

	// cards := newDeck()
	// // fmt.Println(cards.toString())
	// cards.saveToFile("my_cards")

	// cards := newDeckFromFile("my")
	// cards.print()

	cards := newDeck()
	cards.shuffle()
	cards.print()
}

// func newCard() string {
// 	return "Five of Diamonds"
// }
