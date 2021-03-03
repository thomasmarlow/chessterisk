$('#board-main').on('click', '.board-ally-piece', function() {
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
            $(this).addClass('btn-info')
        }
    });
};

const board_reset_all_movable = () => {
    $('.board-movable-square').each(function () {
        $(this).removeClass('btn-warning')
        $(this).removeClass('board-movable-square')
        if ($(this).hasClass('board-empty-square')) {
            $(this).addClass('btn-outline-secondary')
            $(this).addClass('disabled')
        }
        if ($(this).hasClass('board-enemy-piece')) {
            $(this).addClass('btn-danger')
        }
    });
};

const board_select = (square_to_select) => {
    if (square_to_select.hasClass('btn-info')) {
        square_to_select.removeClass('btn-info')
    }
    square_to_select.addClass('btn-dark')
    square_to_select.addClass('board-selected')
};

const board_make_movable_squares_for = (selected_ally_piece) => {
    $('.board-empty-square').each(function () {
        if ($(this).hasClass('btn-outline-secondary')) {
            $(this).removeClass('btn-outline-secondary')
            $(this).removeClass('disabled')
            $(this).addClass('btn-warning')
            $(this).addClass('board-movable-square')
        }
    });
};

$('#board-main').on('click', '.board-movable-square', function () {
    let selected_ally_piece = $('.board-selected')
    test_logger(selected_ally_piece)
    if (selected_ally_piece) {
        if (board_can_move(selected_ally_piece, $(this))) {
            board_make_move(selected_ally_piece, $(this))
            board_reset_all_movable()
        }
    }
});

const board_can_move = (selected_ally_piece, movable_square) => {
    return true
};

const board_make_move = (selected_ally_piece, movable_square) => {
    let can_move = false
    if (movable_square.hasClass('board-empty-square')) {
        movable_square.removeClass('board-empty-square')
        movable_square.removeClass('board-movable-square')
        movable_square.removeClass('btn-warning')
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
        movable_square.addClass('btn-info')
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
    return false
};

const test_logger = (to_log) => {
    if (false) {
        console.log(to_log)
    }
};

$(document).ready(function() {
    // TODO
});