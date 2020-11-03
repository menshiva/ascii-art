from collections import namedtuple
import pytest

import space_motion

SpaceObject = namedtuple('SpaceObject', 'name mass x y vx vy color')
Force = namedtuple('Force', 'fx fy')

#Reference quantities
au = 1.495e11 #astronomical unit, approximately distance from earth to sun [m]
m_sun=1.989e30 #mass of the sun [kg]
m_earth = 5.972e24 #mass of the earth [kg]
earth_radius = 6378e3
speed_earth = 30.0e3 #speed of earth (relative to sun) [m/s]
day = 24*3600 #[s]


def test_calculate_force1():
    #gravitational force that earth acts on 1kg object on the earth sufrace
    earth = SpaceObject(name='earth', mass=1.0*m_earth, x=0.0, y=0.0, vx=0.0, vy=0.0, color='b')
    kilo = SpaceObject(name='kilo', mass=1.0, x=0.0, y=earth_radius, vx=0, vy=0, color='k')
    target = 9.81
    force = space_motion.calculate_force(earth, kilo)
    print(force.fy)
    assert abs(target - force.fy) <= 0.02


def test_calculate_force2():
    #are the force opposite?
    sun = SpaceObject(name='sun', mass=1.0*m_sun, x=0.0, y=au, vx=0.0, vy=0, color='y')
    earth = SpaceObject(name='earth', mass=1.0*m_earth, x=0.0, y=0.0, vx=0.0, vy=0.0, color='b')

    force1 = space_motion.calculate_force(sun, earth)
    force2 = space_motion.calculate_force(earth, sun)
    print(force1.fy, force2.fy)
    assert abs(force1.fy + force2.fy) <= 1.0e-6


def test_update_space_object1():
    #no force, no movement, has to be the same
    kilo = SpaceObject(name='kilo', mass=1.0, x=0.0, y=0.0, vx=0, vy=0, color='black')
    force = Force(fx=0.0, fy=0.0)
    assert kilo == space_motion.update_space_object(kilo, force, 1)


def test_update_space_object2():
    #no force but moving, has to be shifted by 1 second, forces the same
    kilo = SpaceObject(name='kilo', mass=1.0, x=0.0, y=0.0, vx=10.0, vy=20.0, color='black')
    force = Force(fx=0.0, fy=0.0)
    target = SpaceObject(name='kilo', mass=1.0, x=10.0, y=20.0, vx=10.0, vy=20.0, color='black')
    assert target == space_motion.update_space_object(kilo, force, 1)


def test_update_space_object3():
    #force working against the moving object, should stop it
    kilo = SpaceObject(name='kilo', mass=1.0, x=0.0, y=0.0, vx=10.0, vy=0.0, color='black')
    force = Force(fx=-10.0, fy=0.0)
    target1 = SpaceObject(name='kilo', mass=1.0, x=0.0, y=0.0, vx=0.0, vy=0.0, color='black')
    target2 = SpaceObject(name='kilo', mass=1.0, x=5.0, y=0.0, vx=0.0, vy=0.0, color='black')
    result = space_motion.update_space_object(kilo, force, 1)
    assert (target1 == result) or (target2 == result)


def test_simulate_motion1():
    sun = SpaceObject(name='sun', mass=1.0*m_sun, x=0.0, y=au, vx=0.0, vy=0, color='y')
    earth = SpaceObject(name='earth', mass=1.0*m_earth, x=0.0, y=0.0, vx=0.0, vy=0.0, color='b')

    motion = space_motion.simulate_motion(day, 2, earth, sun)
    res = next(motion)
    assert abs(res['earth'][1] - 44337509) <= 1
    assert abs(res['sun'][1] - 149499999866) <= 1

def test_simulate_motion2():
    sun = SpaceObject(name='sun', mass=1.0*m_sun, x=0.0, y=au, vx=0.0, vy=0, color='y')
    earth = SpaceObject(name='earth', mass=1.0*m_earth, x=0.0, y=0.0, vx=0.0, vy=0.0, color='b')

    motion = space_motion.simulate_motion(day, 2, earth, sun)

    res1 = next(motion)
    res2 = next(motion)
    assert abs(res2['earth'][1] - 133038837) <= 1
    assert abs(res2['sun'][1] - 149499999600) <= 1


def test_simulate_motion3():
    sun = SpaceObject(name='sun', mass=1.0*m_sun, x=0.0, y=au, vx=0.0, vy=0, color='y')
    earth = SpaceObject(name='earth', mass=1.0*m_earth, x=0.0, y=0.0, vx=0.0, vy=0.0, color='b')

    motion = space_motion.simulate_motion(day, 1, earth, sun)
    next(motion)
    with pytest.raises(StopIteration):
        next(motion) # end of generator
        pytest.fail('Expecting StopIteration')

def test_logging1(capsys):
    log = space_motion.logging('ms')
    decored = log(space_motion.update_space_object)
    kilo = SpaceObject(name='kilo', mass=1.0, x=0.0, y=0.0, vx=0, vy=0, color='black')
    force = Force(fx=0.0, fy=0.0)
    result = decored(kilo, force=force, timestep=1)
    captured = capsys.readouterr()
    target = 'update_space_object - 12 - '
    assert captured.out[:len(target)] == target

def test_logging2(capsys):
    log = space_motion.logging('ms')
    decored = log(space_motion.update_space_object)
    kilo = SpaceObject(name='kilo', mass=1.0, x=0.0, y=0.0, vx=0, vy=0, color='black')
    force = Force(fx=0.0, fy=0.0)
    result = decored(kilo, force=force, timestep=1)
    captured = capsys.readouterr()
    target = 'ms\n'
    assert captured.out[-len(target):] == target


