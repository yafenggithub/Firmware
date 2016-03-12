/***************************************************************************
 *
 *   Copyright (c) 2016 PX4 Development Team. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 * 3. Neither the name PX4 nor the names of its contributors may be
 *    used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 * COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 * OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 * ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 ****************************************************************************/
/**
 * @file followme.cpp
 *
 * Helper class to track and follow a given position
 *
 * @author Jimmy Johnson <catch22@fastmail.net>
 */

#pragma once

#include <controllib/blocks.hpp>
#include <controllib/block/BlockParam.hpp>

#include "navigator_mode.h"
#include "mission_block.h"
#include <lib/mathlib/math/Vector.hpp>
#include <lib/matrix/matrix/Matrix.hpp>

class FollowTarget : public MissionBlock
{

public:
    FollowTarget(Navigator *navigator, const char *name);

    ~FollowTarget();

    virtual void on_inactive();

    virtual void on_activation();

    virtual void on_active();

    enum {
        ACSEND,
        TRACK_POSITION,
        TRACK_VELOCITY,
        TARGET_TIMEOUT
    };

private:
    static constexpr int TARGET_TIMEOUT_INT_S = 10;
    static constexpr int TARGET_ACCEPTANCE_RADIUS_M = 10;

    Navigator *_navigator;
    control::BlockParamFloat _param_min_alt;
    int _current_target_state;
    int _target_motion_position_sub;

    bool _previous_target_gps_pos_valid;
    bool _radius_entered;
    bool _radius_exited;

    uint64_t _last_publish_time;

    math::Vector<3> _current_vel;
    math::Vector<3> _step_vel;
    math::Vector<3> _target_vel;
    math::Vector<3> _target_distance;

    follow_target_s _current_target_motion;
    follow_target_s _previous_target_motion;
    float _dt;

    void track_position();
    void track_velocity();
    void loiter();
    void update_position_sp(math::Vector<3> & vel);
    void update_target_motion();
    void update_target_velocity();
};
