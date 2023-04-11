var ros = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
});

var client = new ROSLIB.Service({
    ros : ros,
    name : '/patrol_service',
    serviceType : 'std_srvs/Trigger'
});
var patrolStateMachine = new smach.StateMachine({
    states: {
        start_patrol: new smach.State({
            enter: function() {
                console.log('Starting patrol...');

                // Call ROS service to start patrol
                var request = new ROSLIB.ServiceRequest();
                client.callService(request, function(result) {
                    console.log('Patrol started!');
                });
            }
        }),

        stop_patrol: new smach.State({
            enter: function() {
                console.log('Stopping patrol...');

                // Call ROS service to stop patrol
                var request = new ROSLIB.ServiceRequest();
                client.callService(request, function(result) {
                    console.log('Patrol stopped!');
                });
            }
        })
    },
    transitions: {
        start_patrol: {
            success: 'stop_patrol'
        },
        stop_patrol: {
            success: 'start_patrol'
        }
    }
});
var startBtn = document.getElementById('start-btn');
var stopBtn = document.getElementById('stop-btn');

startBtn.addEventListener('click', function() {
    patrolStateMachine.execute('start_patrol');
});

stopBtn.addEventListener('click', function() {
    patrolStateMachine.execute('stop_patrol');
});

patrolStateMachine.setInitialState('start_patrol');

