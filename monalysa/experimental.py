
"""
``experimental.py`` module contains functions for implementing algorithms that
are still experimental. No guarantees are made regarding the performance of 
the algorithms in this module.
----
"""
import numpy as np


def get_move_segment_times(vel: np.array, delt: float, speedth: float=0.05,
                           onth: float=0.1, offth: float=0.1,
                           remove_on_before_off: bool=True,
                           durtol: float=0.1) -> np.array:
    """
    Return start and stop indices for different movement segments from velocity data.

    Parameters
    ----------
    vel : np.array
        Velocity data with columns corresponding to different components,
        and rows corresponding to different samples.
    delt : float
        Sampling time of the given velocity data in seconds. This should be a
        positive number.
    speedth : float
        Speed threshold (ratio with respect to maximum speed) for detecting 
        movement segments. Time instants where speed is lower than this 
        threshold multiplied by the max speed are considered rest.
        This should be a number between 0 and 1. The default value is 0.05.
    onth : float
        Time duration threshold in seconds below which movements segments are
        ignored. This should be a positive number. The default value is 0.1.
    offth : float
        Time duration threshold in seconds below which an interval between 
        movements segments are ignored. This should be a positive number. The 
        default value is 0.1.
    remove_on_before_off : bool
        If True, remove short movement segments first, before removing short
        intervals between movement. The default value is True.
    durtol : float
        Percentage of duration before and after a movement segment to consider for
        identifying movement segments. This value should be between 0 and 1. The 
        default value is 0.1.

    Returns
    -------
    np.array
        An (Nx2) array with start and stop indices for different movement segments.
        The first column corresponds to start times, and the second column corresponds
        to stop times.
    """
    # Some helper functions
    def _remove_short_on_segments(segtimes):
        # Remove short ON segments
        segtimes = segtimes[np.diff(segtimes).T[0] > int(onth / delt), :]
        return np.array(segtimes)
    
    def _remove_short_off_segments(segtimes):
        # Remove short OFF segments
        _durs = segtimes[1:, 0] - segtimes[:-1, 1] 
        _outsegtimes = [segtimes[0, :]]
        for i in range(len(segtimes) - 1):
            if _durs[i] > int(offth / delt):
                _outsegtimes.append(segtimes[i+1, :])
            else:
                _outsegtimes[-1][1] = segtimes[i+1, 1]
        return np.array(_outsegtimes)

    assert isinstance(vel, np.ndarray), 'vel must be a numpy array.'
    assert delt > 0, 'delt must be a positive number.'
    assert 0 < speedth < 1, 'speedth must be between 0 and 1.'
    assert onth >= 0, 'onth must be a non-negative number.'
    assert offth >= 0, 'offth must be a non-negative number.'
    assert 0 < durtol < 1, 'durtol must be between 0 and 1.'

    # Speed
    _spd = np.linalg.norm(vel, axis=1)

    # Movement periods.
    _movseg = _spd > 0.05 * np.max(_spd)

    # Get movement segments
    _strts = np.where(np.diff(np.hstack((0, _movseg))) == 1)[0]
    _stpts = np.where(np.diff(np.hstack((_movseg, 0))) == -1)[0]
    strstpts = np.vstack((_strts, _stpts)).T

    # Filter short on or off segments
    if remove_on_before_off:
        # Remove short ON segments
        strstpts = _remove_short_on_segments(strstpts)
        # Remove short OFF segments
        strstpts = _remove_short_off_segments(strstpts)
    else:
        # Remove short OFF segments
        _durs = strstpts[1:, 0] - strstpts[:-1, 1]
        strstpts = strstpts[np.hstack((True, _durs > int(offth / delt))), :]
        # Remove short ON segments
        strstpts = strstpts[np.diff(strstpts).T[0] > int(onth / delt), :]
    
    # Adjust start and end points by extending left and right.
    strstpts_adj = []
    for i in range(len(strstpts)):
        _prevstrt = 0 if i == 0 else strstpts[i-1, 1]
        _currstrt = strstpts[i, 0]
        _currstpt = strstpts[i, 1]
        _nextstpt = len(_movseg) - 1 if i == len(strstpts) - 1 else strstpts[i+1, 0]
        _ddur = int(durtol * (_currstpt - _currstrt))
        _strt_adj = np.max((_prevstrt, _currstrt - _ddur))
        _stpt_adj = np.min((_currstpt + _ddur, _nextstpt))
        strstpts_adj.append([_strt_adj, _stpt_adj])
    return np.array(strstpts_adj)