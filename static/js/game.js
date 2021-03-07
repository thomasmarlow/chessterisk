var board_grid = []
// var position_string = 'bk'
var color_of_turn = ''
var socket
var audio_capture
var audio_block
var audio_move
var is_spectator = false
var min_row = 0
var max_row = 6
var min_col = 0
var max_col = 5
var str_piece_size = 2
var board_ally_styling
var board_enemy_styling
var board_red_styling = 'btn-danger'
var board_blue_styling = 'btn-info'
var board_side = "blue"

$('#board-main').on('click', '.board-ally-piece', function() {
    if ($(this).hasClass('disabled')) {
        return
    }
    board_deselect_all()
    board_reset_all_movable()
    board_select($(this))
    board_make_movable_squares_for($(this))
});

$('#board-main').on('click', '.board-selected', function() {
    board_deselect_all()
    board_reset_all_movable()
});

const board_deselect_all = () => {
    $('.board-ally-piece').each(function () {
        if ($(this).hasClass('btn-dark')) {
            $(this).removeClass('btn-dark')
            $(this).removeClass('board-selected')
            $(this).addClass(board_ally_styling)
        }
    });
};

const board_reset_all_movable = () => {
    $('.board-movable-square').each(function () {
        $(this).removeClass('board-movable-square')
        if ($(this).hasClass('board-empty-square')) {
            $(this).removeClass('btn-secondary')
            $(this).addClass('btn-outline-secondary')
            $(this).addClass('disabled')
        }
        if ($(this).hasClass('board-enemy-piece')) {
            $(this).removeClass('btn-warning')
            $(this).addClass(board_enemy_styling)
        }
    });
};

const board_select = (square_to_select) => {
    if (square_to_select.hasClass(board_ally_styling)) {
        square_to_select.removeClass(board_ally_styling)
    }
    square_to_select.addClass('btn-dark')
    square_to_select.addClass('board-selected')
};

// const board_make_movable_squares_for = (selected_ally_piece) => {
//     $('.board-empty-square').each(function () {
//         if ($(this).hasClass('btn-outline-secondary')) {
//             $(this).removeClass('btn-outline-secondary')
//             $(this).removeClass('disabled')
//             $(this).addClass('btn-secondary')
//             $(this).addClass('board-movable-square')
//         }
//     });
//     $('.board-enemy-piece').each(function () {
//         if ($(this).hasClass(board_enemy_styling)) {
//             $(this).removeClass(board_enemy_styling)
//             $(this).addClass('btn-warning')
//             $(this).addClass('board-movable-square')
//         }
//     });
// };

const board_make_movable_squares_for = (selected_ally_piece) => {
    let self_row = parseInt(selected_ally_piece.attr('id').split('-')[2])
    let self_col = parseInt(selected_ally_piece.attr('id').split('-')[3])
    test_logger({'row_parsed': self_row, 'col_parsed': self_col})
    if (selected_ally_piece.text() == '♚') {
        board_make_movable_squares_for_master(self_row, self_col)
    } else {
        board_make_movable_squares_for_numbered(self_row, self_col, parseInt(selected_ally_piece.text()))
    }
};

const board_make_movable_squares_for_master = (self_row, self_col) => {
    board_possible_moves_2s(self_row, self_col)
    board_possible_moves_1d(self_row, self_col)
}

const board_make_movable_squares_for_numbered = (self_row, self_col, number) => {
    test_logger(['is even', number, is_even(number)])
    if (is_even(number)) {
        board_possible_moves_1s(self_row, self_col)
    } else {
        board_possible_moves_1d(self_row, self_col)
    }
}

const board_possible_moves_2s = (self_row, self_col) => {
    board_movable_if_applies(self_row+2, self_col)
    board_movable_if_applies(self_row-2, self_col)
    board_movable_if_applies(self_row, self_col+2)
    board_movable_if_applies(self_row, self_col-2)
}

const board_possible_moves_1s = (self_row, self_col) => {
    board_movable_if_applies(self_row+1, self_col)
    board_movable_if_applies(self_row-1, self_col)
    board_movable_if_applies(self_row, self_col+1)
    board_movable_if_applies(self_row, self_col-1)
}

const board_possible_moves_1d = (self_row, self_col) => {
    board_movable_if_applies(self_row+1, self_col+1)
    board_movable_if_applies(self_row+1, self_col-1)
    board_movable_if_applies(self_row-1, self_col+1)
    board_movable_if_applies(self_row-1, self_col-1)
}


const board_movable_if_applies = (row, col) => {
    test_logger({row, col})
    if (row < min_row || row >= max_row) return
    if (col < min_col || col >= max_col) return
    let square = $(`#board-square-${row}-${col}`)
    test_logger(square)
    if (square.hasClass('board-empty-square')) {
        test_logger('in empty')
        square.removeClass('btn-outline-secondary')
        square.removeClass('disabled')
        square.addClass('btn-secondary')
        square.addClass('board-movable-square')
    }
    if (square.hasClass('board-enemy-piece')) {
        test_logger('in enemy')
        square.removeClass(board_enemy_styling)
        square.addClass('btn-warning')
        square.addClass('board-movable-square')
    }
}

const is_even = (number) => {
    return number % 2 == 0
}

$('#board-main').on('click', '.board-movable-square', function () {
    let selected_ally_piece = $('.board-selected')
    test_logger(selected_ally_piece)
    test_logger(get_coords_string(selected_ally_piece))
    test_logger(get_coords_string($(this)))

    if (selected_ally_piece) {
        socket.emit('make move', {
            game_id: $('#board-main').attr('data-game-id'),
            coords_from: get_coords_string(selected_ally_piece),
            coords_to: get_coords_string($(this))
        })
        // board_make_move(selected_ally_piece, $(this))
        // board_reset_all_movable()
    }
}); 

// TODO: this is horrible and needs a better solution... possibly on framework migration?
const get_coords_string = (square) => {
    if (board_side == 'red') {
        return square.attr('id').split('-')[2]+square.attr('id').split('-')[3]
    }
    console.log(square.attr('id'))
    let row = max_row - parseInt(square.attr('id').split('-')[2]) - 1
    let col = max_col - parseInt(square.attr('id').split('-')[3]) - 1
    console.log(row, col)
    return row.toString()+col.toString()
}

const board_make_move = (selected_ally_piece, movable_square) => {
    let can_move = false
    if (movable_square.hasClass('board-empty-square')) {
        movable_square.removeClass('board-empty-square')
        movable_square.removeClass('board-movable-square')
        movable_square.removeClass('btn-secondary')
        can_move = true
    }
    if (movable_square.hasClass('board-enemy-piece')) {
        can_move = board_attack(selected_ally_piece, movable_square)
        if (can_move) {
            movable_square.removeClass('board-enemy-piece')
            movable_square.removeClass('board-movable-square')
            movable_square.removeClass('btn-warning')
        }
    }
    if (can_move) {
        movable_square.addClass('board-ally-piece')
        movable_square.addClass(board_ally_styling)
        selected_ally_piece.removeClass('board-ally-piece')
        selected_ally_piece.removeClass('btn-dark')
        selected_ally_piece.removeClass('board-selected')
        selected_ally_piece.addClass('board-empty-square')
        selected_ally_piece.addClass('btn-outline-secondary')
        selected_ally_piece.addClass('disabled')
        movable_square.text(selected_ally_piece.text())
        selected_ally_piece.text('')
    }
};

const board_attack = (selected_ally_piece, movable_square) => {
    return true
};

const test_logger = (to_log) => {
    if (false) {
        console.log(to_log)
    }
};

$(document).ready(function() {
    audio_capture = $('#audio-rasp')[0]
    audio_block = $('#audio-clack')[0]
    audio_move = $('#audio-pop')[0]
    board_side = get_board_side()
    if (board_side == "red") {
        board_ally_styling = board_red_styling
        board_enemy_styling = board_blue_styling
    } else {
        test_logger('ally styling to blue')
        board_ally_styling = board_blue_styling
        board_enemy_styling = board_red_styling
    }
    get_position()
    is_spectator = ($('#board-main').attr('data-is-viewer') == 'True')
    if ( is_viewer() && $('#board-main').attr('data-winner') == 'None' ) {
        $('#board-info-display').text('entered as spectator')
    }
    socket = io();
    socket.emit('join game', {game_id: $('#board-main').attr('data-game-id')})
    socket.on('move made', function(json_received) {
        console.log('inside move made')
        position_string=json_received.position
        color_of_turn=json_received.color_of_turn
        console.log('json_received')
        render_board()
        if (json_received.hasOwnProperty('attack_result')) {
            display_attack_result(json_received.attack_result)
            if ('captures:' == json_received.attack_result.split(' ')[1]) {
                audio_capture.play()
            }
            if ('blocks:' == json_received.attack_result.split(' ')[1]) {
                audio_block.play()
            }
        } else {
            $('#board-info-display').removeClass('alert-dark')
            $('#board-info-display').removeClass('alert-primary')
            $('#board-info-display').removeClass('alert-danger')
            $('#board-info-display').addClass('alert-dark')
            $('#board-info-display').text('...')
            audio_move.play()
        }
        if (json_received.hasOwnProperty('winner_color')) {
            display_winner(json_received.winner_color)
        }
    });
    socket.on('viewer mode', function() {
        console.log('viewer mode event triggered')
        $('#board-main').attr('data-is-viewer', 'True')
        render_board()
    })
    // set_initial_message();
});

const set_initial_message = () => {
    if ( $('#board-main').attr('data-is-inviter') != "" ) {
        $('#board-info-display').text('share your url with your friend')
        return
    }
    $('#board-info-display').text('entered game by invitation')
}

const display_attack_result = (attack_result) => {
    if (attack_result.split(' ')[0] == 'red') {
        $('#board-info-display').removeClass('alert-dark')
        $('#board-info-display').removeClass('alert-primary')
        $('#board-info-display').removeClass('alert-danger')
        $('#board-info-display').addClass('alert-danger')
    } else {
        $('#board-info-display').removeClass('alert-dark')
        $('#board-info-display').removeClass('alert-primary')
        $('#board-info-display').removeClass('alert-danger')
        $('#board-info-display').addClass('alert-primary')
    }
    $('#board-info-display').text(attack_result)
}

const display_winner = (winner_color) => {
    $('#board-info-display').removeClass('alert-dark')
    $('#board-info-display').removeClass('alert-primary')
    $('#board-info-display').removeClass('alert-danger')
    if (winner_color == 'red') {
        $('#board-info-display').addClass('alert-danger')
        $('#board-info-display').text('red won!')
    } else {
        $('#board-info-display').addClass('alert-primary')
        $('#board-info-display').text('blue won!')
    }
    disable_all_squares()
}

const board_square_set = (row, col, piece_string) => {
    test_logger([row, col, piece_string])
    let board_square = $(`#board-square-${row}-${col}`)
    if (piece_string == 'es') {
        board_square.addClass('board-empty-square')
        board_square.addClass('btn-outline-secondary')
        board_square.addClass('disabled')
        return
    } else {
        board_square.removeClass('board-empty-square')
        board_square.removeClass('btn-outline-secondary')
        board_square.removeClass('disabled')
    }
    set_piece_symbol(board_square, piece_string)
    if (get_piece_color(piece_string) == board_side) {
        board_square.addClass('board-ally-piece')
    } else {
        board_square.addClass('board-enemy-piece')
    }
    if (get_piece_color(piece_string) == 'red') {
        board_square.addClass(board_red_styling)
    } else {
        board_square.addClass(board_blue_styling)
    }
}

const set_piece_symbol = (board_square, piece_string) => {
    if (piece_string.charAt(1) == 'k') {
        board_square.append('<i class="fas fa-crown" style="font-size: 5vmin;"></i>')
    } else {
        board_square.text(piece_string.charAt(1))
    }
}

const get_piece_color = (piece_string) => {
    if (piece_string.charAt(0) == 'b') {
        return 'blue'
    }
    return 'red'
}

const get_position = () => { // could be replaced by 'join game'
    // $.get( "/game/"+ $('#board-main').attr('data-game-id') +"/position", function(json_response) {
    //     test_logger(json_response)
    //     position_string=json_response.position
    // });
    $.ajax({
        // async: false,
        type: 'GET',
        url: "/game/"+ $('#board-main').attr('data-game-id') +"/position",
        success: function(json_response) {
            test_logger(json_response)
            position_string=json_response.position
            color_of_turn=json_response.color_of_turn
            render_board()
        }
    });
}

const render_board = () => {
    reset_whole_board()
    paint_bg_gradient()
    for (let row = min_row; row < max_row; row++) {
        for (let col = min_col; col < max_col; col++) {
            if (board_side == 'red') {
                // board_square_set(row, col, board_grid[row][col]);
                test_logger('red is bottom')
                board_square_set(row, col, position_string.slice(str_piece_size*(row*max_col+col), str_piece_size*(row*max_col+col+1)))
            } else {
                test_logger('blue is bottom')
                // board_square_set(max_row-row-1, max_col-col-1, board_grid[row][col]);
                board_square_set(max_row-row-1, max_col-col-1, position_string.slice(str_piece_size*(row*max_col+col), str_piece_size*(row*max_col+col+1)))
            }
        }
    }
    if (color_of_turn != board_side) {
        disable_all_squares()
    }
    if ( is_viewer() ) {
        disable_all_squares()
    }
    check_if_winner()
}

const paint_bg_gradient = () => {
    if (board_side == 'red') {
        if (color_of_turn == 'red') {
            board_set_bg('grad-red-bottom')
        } else {
            board_set_bg('grad-blue-top')
        }
    } else {
        if (color_of_turn == 'red') {
            board_set_bg('grad-red-top')
        } else {
            board_set_bg('grad-blue-bottom')
        }
    }
}

const board_set_bg = (grad_class) => {
    $('#board-bg').removeClass('grad-red-bottom')
    $('#board-bg').removeClass('grad-red-top')
    $('#board-bg').removeClass('grad-blue-bottom')
    $('#board-bg').removeClass('grad-blue-top')
    $('#board-bg').addClass(grad_class)
}

const is_viewer = () => {
    // console.log('is viewer', $('#board-main').attr('data-is-viewer'), $('#board-main').attr('data-is-viewer') == 'True')
    // if ( $('#board-main').attr('data-is-viewer') == 'True' ) {
    //     return true
    // }
    // return false
    console.log('is spectator: ', is_spectator)
    return is_spectator
}

const check_if_winner = () => {
    if ( $('#board-main').attr('data-winner') == 'red' ) {
        $('#board-info-display').removeClass('alert-dark')
        $('#board-info-display').removeClass('alert-primary')
        $('#board-info-display').removeClass('alert-danger')
        $('#board-info-display').addClass('alert-danger')
        console.log('check if winner: red')
        disable_all_squares()
    }
    if ( $('#board-main').attr('data-winner') == 'blue' ) {
        $('#board-info-display').removeClass('alert-dark')
        $('#board-info-display').removeClass('alert-primary')
        $('#board-info-display').removeClass('alert-danger')
        $('#board-info-display').addClass('alert-primary')
        console.log('check if winner: blue')
        disable_all_squares()
    }
}

const disable_all_squares = () => {
    $('.board-square').each(function() {
        if (!($(this).hasClass('disabled'))) {
            $(this).addClass('disabled')
        }
    });
}

const reset_whole_board = () => {
    $('.board-square').each(function() {
        $(this).removeClass()
        $(this).text('')
        $(this).addClass('btn board-square board-empty-square btn-outline-secondary disabled')
    });
    $('.board-square').empty()
}

// const board_square_set = (row, col, board_square_data) => {
//     test_logger([row, col, board_square_data])
//     let board_square = $(`#board-square-${row}-${col}`)
//     if (board_square_data.type == 'empty') {
//         board_square.addClass('board-empty-square')
//         board_square.addClass('btn-outline-secondary')
//         board_square.addClass('disabled')
//         return
//     } else {
//         board_square.removeClass('board-empty-square')
//         board_square.removeClass('btn-outline-secondary')
//         board_square.removeClass('disabled')
//     }
//     board_square.text(board_square_data.text)
//     if (board_square_data.type == board_side) {
//         board_square.addClass('board-ally-piece')
//     } else {
//         board_square.addClass('board-enemy-piece')
//     }
//     if (board_square_data.type == 'red') {
//         board_square.addClass(board_red_styling)
//     } else {
//         board_square.addClass(board_blue_styling)
//     }
// }

const get_board_side = () => {
    test_logger(['side', $('#board-main').attr('data-color')]) // TODO: rename all 'side' to 'color'
    return $('#board-main').attr('data-color')
}

const self_generate_board_grid = () => {
    for (let row = 0; row < 6; row++) {
        board_grid[row] = []
    }
    board_grid[0][0] = {
        'type': 'red',
        'text': '5',
        'row': 0,
        'col': 0
    }
    board_grid[0][1] = {
        'type': 'red',
        'text': '6',
        'row': 0,
        'col': 1
    }
    board_grid[0][2] = {
        'type': 'red',
        'text': '7',
        'row': 0,
        'col': 2
    }
    board_grid[0][3] = {
        'type': 'red',
        'text': '8',
        'row': 0,
        'col': 3
    }
    board_grid[0][4] = {
        'type': 'red',
        'text': '9',
        'row': 0,
        'col': 4
    }
    board_grid[1][0] = {
        'type': 'red',
        'text': '♚',
        'row': 1,
        'col': 0
    }
    board_grid[1][1] = {
        'type': 'red',
        'text': '1',
        'row': 1,
        'col': 1
    }
    board_grid[1][2] = {
        'type': 'red',
        'text': '2',
        'row': 1,
        'col': 2
    }
    board_grid[1][3] = {
        'type': 'red',
        'text': '3',
        'row': 1,
        'col': 3
    }
    board_grid[1][4] = {
        'type': 'red',
        'text': '4',
        'row': 1,
        'col': 4
    }
    for (let row = 2; row < 4; row++) {
        for (let col = 0; col < 5; col++) {
            board_grid[row][col] = {
                'type': 'empty',
                'row': row,
                'col': col
            }
        }
    }
    board_grid[4][0] = {
        'type': 'blue',
        'text': '5',
        'row': 4,
        'col': 0
    }
    board_grid[4][1] = {
        'type': 'blue',
        'text': '6',
        'row': 4,
        'col': 1
    }
    board_grid[4][2] = {
        'type': 'blue',
        'text': '7',
        'row': 4,
        'col': 2
    }
    board_grid[4][3] = {
        'type': 'blue',
        'text': '8',
        'row': 4,
        'col': 3
    }
    board_grid[4][4] = {
        'type': 'blue',
        'text': '9',
        'row': 4,
        'col': 4
    }
    board_grid[5][0] = {
        'type': 'blue',
        'text': '♚',
        'row': 5,
        'col': 0
    }
    board_grid[5][1] = {
        'type': 'blue',
        'text': '1',
        'row': 5,
        'col': 1
    }
    board_grid[5][2] = {
        'type': 'blue',
        'text': '2',
        'row': 5,
        'col': 2
    }
    board_grid[5][3] = {
        'type': 'blue',
        'text': '3',
        'row': 5,
        'col': 3
    }
    board_grid[5][4] = {
        'type': 'blue',
        'text': '4',
        'row': 5,
        'col': 4
    }
}