#TODO

 class nicomotion.Mover.Mover(robot, stiff_off=False, path_to_config_file='mover.conf')

    Bases: object

    calc_move_file(fname, target_fname, number)

    freeze_joints(subsetfname=None, stiffness=None, unfreeze=False)

    move_file_position(fname, subsetfname=None, move_speed=0.04)

    move_position(target_positions, speed, real=True)

    play_movement(fname, subsetfname=None, move_speed=0.04)

    record_movement(fname=None)

    record_position(fname=None)
    