use std::collections::HashMap;

fn main() {
    let string = String::from("banana");

    let aux = character_occurences_in(string);

    println!("{:#?}", aux);
}

fn character_occurences_in(word: String) -> HashMap<char, i32> {
    let mut occurences = HashMap::<char, i32>::new();

    for character in word.chars() {
        let counter = occurences.entry(character).or_insert(0);
        *counter += 1;
    }
    occurences
}
