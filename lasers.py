"""
description: A game to place 'n' 3-way lasers on the grid
         such that they cover the highest sum in the grid
language: python3
author: Lahari Chepuri(lc8104 @ RIT.EDU)
author: Smita Subhadarshinee Mishra(sm8528 @ RIT.EDU)
"""

def search_index( data, val, left, right, index_to_insert ):
    """
    Finds the index to insert value, the data list will always be sorted at all time
    :param data: The Sorted list
    :param val: The value to insert
    :param left: The first position of the array segment
    :param right: The last position of array segment
    :param index_to_insert: The index where the value has to be inserted
    :pre: data will be initialized to all zeros
    :post: sorted data with the highest values considered
    :return: returns the index where we have to insert.
    """
    if left > right:
        return index_to_insert
    midindex = (left + right) // 2
    if data[ midindex ][ 0 ] == val:
        return midindex

    if val > data[ midindex ][ 0 ]:
        return search_index( data, val, midindex + 1, right, midindex + 1 )
    else:
        return search_index( data, val, left, midindex - 1, index_to_insert )

def top_n_hits( possible_hits, number_of_lasers ):
    """
    Finds of the top best hits from the possible hits
    :param possible_hits:  All the possible hits
    :param number_of_lasers: No of best laser hits required
    :return: Sorted array of number_of_lasers best hits
    """
    sorted_list = [ (0, '') ] * number_of_lasers
    for hit in possible_hits:
        index_to_insert = search_index( sorted_list, hit[ 0 ], 0, len( sorted_list ) - 1, -1 )
        if index_to_insert >= 0:
            sorted_list.insert( index_to_insert, hit )
            del sorted_list[ 0 ]
    return sorted_list;

def get_possible_hits( grid ):
    """
    Finds all the possible hits
    :param grid: The puzzle grid 2D array
    :return: All the possible hits
    """
    possible_hits = [ ]
    size = len( grid )
    for x in range( size ):
        for y in range( size ):
            if not ((x == 0 or x == size - 1) and (y == 0 or y == size - 1)):
                if x == 0:
                    (max_sum, facing) = (
                    int( grid[ x ][ y + 1 ] ) + int( grid[ x ][ y - 1 ] ) + int( grid[ x + 1 ][ y ] ), 'facing south')
                elif y == 0:
                    (max_sum, facing) = (
                    int( grid[ x ][ y + 1 ] ) + int( grid[ x + 1 ][ y ] ) + int( grid[ x - 1 ][ y ] ), 'facing east')
                elif x == size - 1:
                    (max_sum, facing) = (
                    int( grid[ x ][ y + 1 ] ) + int( grid[ x ][ y - 1 ] ) + int( grid[ x - 1 ][ y ] ), 'facing north')
                elif y == size - 1:
                    (max_sum, facing) = (
                    int( grid[ x ][ y - 1 ] ) + int( grid[ x + 1 ][ y ] ) + int( grid[ x - 1 ][ y ] ), 'facing west')
                else:
                    facing, max_sum = best_hit_direction( grid, x, y )
                possible_hits.append( (max_sum, (y, x), facing) )
    return possible_hits

def best_hit_direction( grid, x, y ):
    """
    Gets the direction in which we get the largest hit
    :param grid: The input puzzle
    :param x: The x coordinates of the square
    :param y: The y coordinate of square
    :return: A tuple of the sum, the coordinate and direction of best hit
    """
    data = [ (0, '') ] * 3
    max_sum = 0
    facing = ''
    #get all the possible adjasent hits
    possible = [ (grid[ x ][ y + 1 ], 'facing west'), (grid[ x ][ y - 1 ], 'facing east'),
                 (grid[ x + 1 ][ y ], 'facing north'), (grid[ x - 1 ][ y ], 'facing south') ]
    #sort and get the best 3 sides
    for p in possible:
        # if the particular hit has a greater integer value than any other hit then get the position to insert
        index_to_insert = search_index( data, int( p[ 0 ] ), 0, len( data ) - 1, -1 )
        if index_to_insert >= 0:
            #insert at the given position
            data.insert( index_to_insert, (int( p[ 0 ] ), p[ 1 ]) )
            # consider the facing of the one getting removed
            (max_sum, facing) = (max_sum + int( p[ 0 ] ) - data[ 0 ][ 0 ], data[ 0 ][ 1 ])
            # delete is the first one as it would be the least one
            del data[ 0 ]
        else:
            (max_sum, facing) = (max_sum, p[ 1 ])
    return facing, max_sum

def play_laser( grid, no_of_lasers ):
    """
    Plays the puzzle game and prints output
    :param grid: The input puzzle grid
    :param no_of_lasers: The numbers of lasers to be placed
    """
    possible_hits = get_possible_hits( grid )
    if no_of_lasers <= len(possible_hits) :
        best_hits = top_n_hits(possible_hits, no_of_lasers)
    else:
        print("you can pass only", len(possible_hits), "lasers")
        print(len(possible_hits), "laser placements would be: ")
        best_hits = top_n_hits(possible_hits, len(possible_hits))
    for hit in best_hits[ len( best_hits ) - 1::-1 ]:
        print( hit[ 1 ], ' ', hit[ 2 ] )

def parse_args( file_name ):
    """
    Reads the file for the puzzle grid
    :param file_name: The file name to be read
    :return: 2D array of the grid
    """
    grid = [ ]
    with open( file_name, 'r' ) as grid_file:
        for line in grid_file:
            grid.append( line.split() )
    return grid

def main():
    file_name = input( 'Please enter the file name: ' )
    grid = parse_args( file_name )
    no_of_lasers = int( input( 'Number of lasers to place: ' ) )
    play_laser( grid, no_of_lasers )

if __name__ == '__main__':
    main()