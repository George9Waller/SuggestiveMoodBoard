from colorharmonies import (Color, complementaryColor, triadicColor, splitComplementaryColor, tetradicColor,
                            analogousColor, monochromaticColor)
from models import Idea


def suggestions_algorithm(board, number_requested=600):
    """Algorithm handler"""
    weighted_ideas = get_ideas(board)  # dictionary of unique colours from ideas with their calculated weightings
    generated_suggestions = generate_suggestions(weighted_ideas)
    final_suggestions = present_suggestions(generated_suggestions, number_requested)
    return final_suggestions


def get_ideas(board):
    """1. Get Ideas - takes board object"""
    # 1a query database for all ideas with colour
    ideas = Idea.get_colour_ideas_by_board(board)

    # 1c extract colours into dictionary with weighting
    data = dict()

    if len(ideas) == 0:
        add_colour_to_dictionary(data, '#ffffff')  # add white if there are no colour tags
    else:
        for idea in ideas:
            add_colour_to_dictionary(data, Idea.get_colour(idea))

    """sort dictionary by value descending"""
    return sort_dictionary_by_desc_value(data)


def generate_suggestions(data):
    """3. Generate Suggestions - takes dictionary of key:colour and value:weighting and returns an ordered dictionary"""
    """Using this library for the colour generation: https://github.com/baptistemanteau/colorharmonies"""

    suggestion_results = dict()
    for key in data:
        hex_colour = key.lstrip('#')
        # https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
        current_colour = Color(tuple(int(hex_colour[i:i + 2], 16) for i in (0, 2, 4)), "", "")

        # 3b calculate suggestions
        # complimentary colour - returns 1
        add_colour_to_dictionary(suggestion_results, tuple(complementaryColor(current_colour)),
                                 data[key])

        # triadic colour - returns 2
        for new_triadic_colour in triadicColor(current_colour):
            add_colour_to_dictionary(suggestion_results, tuple(new_triadic_colour), data[key])

        # split complementary colour - returns 2
        for new_split_complementary_colour in splitComplementaryColor(current_colour):
            add_colour_to_dictionary(suggestion_results, tuple(new_split_complementary_colour),
                                     data[key])

        # tetradic colour - returns 3
        for new_tetradic_colour in tetradicColor(current_colour):
            add_colour_to_dictionary(suggestion_results, tuple(new_tetradic_colour),
                                     data[key])

        # analogous colour - returns 2
        for new_analogous_colour in analogousColor(current_colour):
            add_colour_to_dictionary(suggestion_results, tuple(new_analogous_colour),
                                     data[key])

        # monochromatic colour - returns list
        for new_monochromatic_colour in monochromaticColor(current_colour):
            add_colour_to_dictionary(suggestion_results, tuple(new_monochromatic_colour),
                                     data[key])

    # 3c sort array by weighting
    return sort_dictionary_by_desc_value(suggestion_results)


def present_suggestions(data, number_requested):
    """5. Present suggestions takes an ordered dictionary of key:colour and value:weighting and returns a list of
    html hex colours """
    colour_list = [item[0] for item in list(data.items())[:number_requested]]

    # concatenate hex as 4th element in tuple using list comprehension
    return [elem + (convert_tuple_to_rgb_hex(elem),) for elem in colour_list]


def sort_dictionary_by_desc_value(dictionary):
    """sorts a given dictionary in descending order of value"""
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}


def add_colour_to_dictionary(dictionary, colour, initial_value=0.2):
    """uses algorithm to add unique colours to dictionary or update weighting - takes dictionary and colour"""
    if colour in dictionary:
        """Update value using equation ans * (0.8 + ((1 / ans) / 5))"""
        value = dictionary.get(colour, None)
        value = value * (0.8 + ((1 / value) / 5))
        dictionary[colour] = value
    else:
        dictionary[colour] = initial_value
    return dictionary


def convert_tuple_to_rgb_hex(rgb_tuple):
    """converts a tuple in the format (r, g, b) to html hex"""
    return '#%02x%02x%02x' % rgb_tuple
