import { useState, useEffect } from 'react';
import './Consumotable.css'
import type { rowObj, respObj} from '../assets/customtypes';

const APIdata = () => {
  const [resp, setresp] = useState(new Object as respObj)
  useEffect(() => {
      fetch('api/consumtion/')
         .then((response) => response.json())
         .then((data) => {
            setresp(data);
         })
         .catch((err) => {
            console.log(err.message);
         });
   }, []);
   data = new Array<rowObj>()
   for (let key of Object.keys(resp)){
    let consumo = new Array
    resp[key].forEach((elem) => consumo.push(elem.valor))
    let total = consumo.reduce((x, y) => x + y)
    let avg = total / consumo.length
    let max = Math.max(...consumo)
    data.push ({
      uid: Number(key),
      total: total,
      avg: avg,
      max: max
    })
   }
}

let data =new Array<rowObj>()


function RenderRows() {
  APIdata()
  const rows = data.map( elem => 
    <tr key={elem.uid}>
      <td>{elem.uid }</td>
      <td>{elem.total.toFixed(2)}</td>
      <td>{elem.avg.toFixed(2)}</td>
      <td>{elem.max.toFixed(2)}</td>
    </tr>
  )
  return (
    <tbody>
      {rows}
    </tbody>
  )
}

export default function Consumotable(){
    return (
    <>
      <table>
        <thead>
          <tr>
              <th>Participante</th>
              <th>Consumo total</th>
              <th>Consumo medio</th>
              <th>Consumo máx</th>
          </tr>
        </thead>
        <RenderRows />
        <tfoot>
          <tr>
            <th colSpan={4}>Consumo anual en kw</th>
          </tr>
        </tfoot>
      </table>
    </>
  )
}