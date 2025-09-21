export type rowObj = {'uid':number, 'total': number, 'avg': number, 'max':number}
export type respObj = {[key:string]: Array<{ valor:number, timestamp: Date}>}
export type datastruct = Array<{timestamp:number, generacion:number, [key:string]:number}>
export type filterstruct = {[key:string]:boolean}
export type palettestruct = {[key:string]:string}