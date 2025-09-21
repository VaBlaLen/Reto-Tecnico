import { useState, useEffect } from 'react';
import { ComposedChart, Area, YAxis, XAxis, Legend, Tooltip, Line } from 'recharts';
import './Chart.css';
import { useRandomColor } from '../helpers/RandomizeColor';
import type { filterstruct, datastruct, palettestruct} from '../assets/customtypes';

const CustomizedAxisTick = ({ x, y, stroke, payload }) => {
  return (
      <g transform={`translate(${x},${y})`}>
        <text x={0} y={5} dy={16} textAnchor="middle" fill="#666">
          {new Date(payload.value * 1000).toLocaleDateString()}
        </text>
        <text x={0} y={20} dy={16} textAnchor="middle" fill="#666">
          {new Date(payload.value * 1000).toLocaleTimeString()}
        </text>
      </g>
    );
};

const CustomTooltip = ({ active, payload, label }) => {
  const isVisible = active && payload && payload.length;
  return (
    <div className="custom-tooltip" style={{ visibility: isVisible ? 'visible' : 'hidden' }}>
      {isVisible && (
        <>
          <p className="label">{`${new Date(label * 1000).toLocaleDateString()}`} <br/> {`${new Date(label * 1000).toLocaleTimeString()}`}</p>
          {
            payload.map((elem: { dataKey: string; value: number; })=>(
              <p className="label">{`${elem.dataKey}:${elem.value.toFixed(2)} Kw`}</p>
            ))
          }
         </>
      )}
    </div>
  );
};


var lowerbound:number, upperbound:number

export default function Chart() {
    const [currentleft, setcurrentleft] = useState(0);
    const [currentright, setcurrentright] = useState(1);
    const [resp, setresp] = useState( [] as datastruct)
    const [filter, setfilter] = useState({} as filterstruct)
    const {generateColor } = useRandomColor()
    const [palette, setPalette] = useState({} as palettestruct)
    useEffect(() => {
      fetch('api/generation/')
         .then((response) => response.json())
         .then((data) => {
            let newpal:palettestruct = {}
            let filterstatus:filterstruct = {}
            let newresp:datastruct = (data as Array<{timestamp:any, generacion:number, [key:string]:number}>).map((value) => {
                return {timestamp: Date.parse(value.timestamp) / 1000, generacion: value.valor}
            })
            filterstatus[`generacion`] = true
            newpal[`generacion`] = generateColor()
            fetch('api/consumtion/')
              .then((response) => response.json())
              .then((data) => {
                  for(let key of Object.keys(data) ){
                    newresp = newresp.map((elem, index) =>{
                      let newelem = {...elem}
                      newelem[`Participante${key}`] = data[key][index].valor
                      return  newelem
                    })
                    filterstatus[`Participante${key}`] = true
                    newpal[`Participante${key}`] = generateColor()
                  }
                  setresp(newresp);
                  lowerbound = newresp[0].timestamp
                  upperbound = newresp[newresp.length-1].timestamp
                  setcurrentleft(lowerbound)
                  setcurrentright(upperbound)
                  setPalette(newpal)
                  setfilter(filterstatus)
              })
              .catch((err) => {
                  console.log(err.message);
              });
         })
         .catch((err) => {
            console.log(err.message);
         });
   }, []);
    return (
      <>
      <ComposedChart width={1200} height={500} data={resp}>
        <XAxis dataKey="timestamp" type='number' height={50}
            domain={[()=>currentleft, ()=>currentright]} allowDataOverflow
            tick={<CustomizedAxisTick />} />
        <YAxis label={{ value: 'KW', angle: -90, position: 'insideLeft' }} scale="symlog"/>
        <Tooltip content={CustomTooltip}/>
        <Legend verticalAlign="top"/>
         {
          Object.keys(filter).map( (f) => {
            if (filter[f]){
              return <Line type="monotone" dataKey={f} stroke={palette[f]} dot={false}/>
            }
          })
        }
      </ComposedChart>
      <div id = "brushcontainer">
        <input className='brushinput' type="text" readOnly value={new Date(currentleft * 1000).toLocaleString()}/>
        <input className='brushinput' type="text" readOnly value={new Date(currentright* 1000).toLocaleString()}/>
      </div>
      <div id="mybrush" className="brush">
        
        <input id="from" type="range" min={lowerbound} max={upperbound-3600} value={currentleft} step={3600}
          onInput={
            () =>
              { 
                let lval = Number((document.getElementById("from") as HTMLInputElement).value)
                let rval = Number((document.getElementById("to") as HTMLInputElement).value)
                setcurrentleft(lval)
                setcurrentright(Math.max(rval, lval+3600))
              }
        }></input>
        <input id="to" type="range" min={lowerbound+3600} max={upperbound} value={currentright} step={3600} 
        onInput={
            () =>
              { 
                let lval = Number((document.getElementById("from") as HTMLInputElement).value)
                let rval = Number((document.getElementById("to") as HTMLInputElement).value)
                setcurrentleft(Math.min(rval-3600, lval))
                setcurrentright(rval)
              }
        }></input>
       
      </div>
      <div id="filter">
        {
          Object.keys(filter).map( (f) => (
            <label className='filterlabel'><input type='checkbox' id={f} value={f} checked={filter[f]} onChange={
              ()=>{
                const auxfilter = {...filter}
                auxfilter[f] = !auxfilter[f]
                setfilter(auxfilter)
              }
            }/>{f}</label>
          ))
        }
      </div>
      </>
   )
}