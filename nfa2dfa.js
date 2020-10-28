const NFA = {
    states:[
        {
            state: "s0",
            final: true
        },
        {
            state: "s1",
            final: true
        },
        {
            state: "s2",
            final: false
        },
    ],
    transitions:[
        {
            from:"s0",
            to:"s1",
            input:0
        },
        {
            from:"s0",
            to:"s1",
            input:1
        },
        {
            from:"s0",
            to:"s2",
            input:1
        },
        {
            from:"s2",
            to:"s2",
            input:1
        },
        {
            from:"s2",
            to:"s1",
            input:0
        }
    ]
}

function nfa2dfa(nfa){
    let dfa = {
        states:[{
            state:["s0"],
            final:nfa.states.filter(state=>state.state==="s0")[0].final
        }],
        transitions:[]
    }
    let i = 0
    while (dfa.states.length > i) {
        const destination0 = findDestination(dfa.states[i].state, 0 ,nfa)
        const destination1 = findDestination(dfa.states[i].state, 1 ,nfa)
        if (destination0.length > 0){
            if(dfa.states.filter(state=>state.state.join("")===destination0.join("")).length===0){
                dfa.states.push({
                    state:destination0,
                    final:checkFinal(destination0,nfa)
                })
            }
            dfa.transitions.push({
                from: dfa.states[i].state,
                input:0,
                to: destination0
            })
        }
        if (destination1.length > 0 ){
            if (dfa.states.filter(state=>state.state.join("")===destination1.join("")).length===0) {
                    
                dfa.states.push({
                    state:destination1,
                    final:checkFinal(destination1,nfa)
                })
            }
            dfa.transitions.push({
                from: dfa.states[i].state,
                input:1,
                to: destination1
            })
        }
        i=i+1
    }
    console.log(JSON.stringify(dfa))

}

function findDestination(start, input, nfa){
    if (typeof start === Object) start = [start]
    const result =  nfa.transitions
    .filter(tran=> tran.input === input && start.indexOf(tran.from)>-1)
    .reduce((acu,cur)=>{
        if (acu.indexOf(cur.to)>-1) return acu
        return [...acu,cur.to]
    },[])
    .sort()
    return result
}


function checkFinal(state, nfa){
    return state.some(state=> nfa.states.filter(ref=>ref.state===state)[0].final)
}

nfa2dfa(NFA)
