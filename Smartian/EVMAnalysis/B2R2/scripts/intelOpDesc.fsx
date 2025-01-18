#!/usr/bin/env fsharpi
#load "../src/Core/TypeExtensions.fs"
#load "../src/Core/RegType.fs"
#load "../src/Core/RegisterID.fs"
#load "../src/Core/WordSize.fs"
#load "../src/Core/AddrRange.fs"
#load "../src/FrontEnd/Intel/IntelRegister.fs"
#load "../src/FrontEnd/Intel/IntelTypes.fs"
(*
  B2R2 - the Next-Generation Reversing Platform

  Copyright (c) SoftSec Lab. @ KAIST, since 2016

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
*)

open B2R2.FrontEnd.Intel

type R = Register

/// Converted to int64 by script
let _Ap = ODModeSize (struct (OprMode.A, OprSize.P))
let _BNDRbnd = ODModeSize (struct (OprMode.BndR, OprSize.Bnd))
let _BNDRMbnd = ODModeSize (struct (OprMode.BndM, OprSize.Bnd))
let _By = ODModeSize (struct (OprMode.B, OprSize.Y))
let _Cd = ODModeSize (struct (OprMode.C, OprSize.D))
let _Dd = ODModeSize (struct (OprMode.D, OprSize.D))
let _E0v = ODModeSize (struct (OprMode.E0, OprSize.V)) (* \x0f\x1f *)
let _Eb = ODModeSize (struct (OprMode.E, OprSize.B))
let _Ed = ODModeSize (struct (OprMode.E, OprSize.D))
let _Edb = ODModeSize (struct (OprMode.E, OprSize.DB))
let _Edw = ODModeSize (struct (OprMode.E, OprSize.DW))
let _Ep = ODModeSize (struct (OprMode.E, OprSize.P))
let _Ev = ODModeSize (struct (OprMode.E, OprSize.V))
let _Ew = ODModeSize (struct (OprMode.E, OprSize.W))
let _Ey = ODModeSize (struct (OprMode.E, OprSize.Y))
let _Gb = ODModeSize (struct (OprMode.G, OprSize.B))
let _Gd = ODModeSize (struct (OprMode.G, OprSize.D))
let _Gv = ODModeSize (struct (OprMode.G, OprSize.V))
let _Gw = ODModeSize (struct (OprMode.G, OprSize.W))
let _Gy = ODModeSize (struct (OprMode.G, OprSize.Y))
let _Gz = ODModeSize (struct (OprMode.G, OprSize.Z))
let _Hdq = ODModeSize (struct (OprMode.H, OprSize.DQ))
let _Hpd = ODModeSize (struct (OprMode.H, OprSize.PD))
let _Hps = ODModeSize (struct (OprMode.H, OprSize.PS))
let _Hqq = ODModeSize (struct (OprMode.H, OprSize.QQ))
let _Hsd = ODModeSize (struct (OprMode.H, OprSize.SD))
let _Hss = ODModeSize (struct (OprMode.H, OprSize.SS))
let _Hx = ODModeSize (struct (OprMode.H, OprSize.X))
let _Ib = ODModeSize (struct (OprMode.I, OprSize.B))
let _Iv = ODModeSize (struct (OprMode.I, OprSize.V))
let _Iw = ODModeSize (struct (OprMode.I, OprSize.W))
let _Iz = ODModeSize (struct (OprMode.I, OprSize.Z))
let _Jb = ODModeSize (struct (OprMode.J, OprSize.B))
let _Jz = ODModeSize (struct (OprMode.J, OprSize.Z))
let _Ma = ODModeSize (struct (OprMode.M, OprSize.A))
let _Md = ODModeSize (struct (OprMode.M, OprSize.D))
let _Mdq = ODModeSize (struct (OprMode.M, OprSize.DQ))
let _Mdqd = ODModeSize (struct (OprMode.M, OprSize.DQD))
let _Mp = ODModeSize (struct (OprMode.M, OprSize.P))
let _Mpd = ODModeSize (struct (OprMode.M, OprSize.PD))
let _Mps = ODModeSize (struct (OprMode.M, OprSize.PS))
let _Mq = ODModeSize (struct (OprMode.M, OprSize.Q))
let _Ms = ODModeSize (struct (OprMode.M, OprSize.S))
let _Mv = ODModeSize (struct (OprMode.M, OprSize.V))
let _Mw = ODModeSize (struct (OprMode.M, OprSize.W))
let _Mx = ODModeSize (struct (OprMode.M, OprSize.X))
let _My = ODModeSize (struct (OprMode.M, OprSize.Y))
let _Mz = ODModeSize (struct (OprMode.M, OprSize.Z))
let _MZxz = ODModeSize (struct (OprMode.MZ, OprSize.XZ))
let _Nq = ODModeSize (struct (OprMode.N, OprSize.Q))
let _Ob = ODModeSize (struct (OprMode.O, OprSize.B))
let _Ov = ODModeSize (struct (OprMode.O, OprSize.V))
let _Pd = ODModeSize (struct (OprMode.P, OprSize.D))
let _Ppi = ODModeSize (struct (OprMode.P, OprSize.PI))
let _Pq = ODModeSize (struct (OprMode.P, OprSize.Q))
let _Qd = ODModeSize (struct (OprMode.Q, OprSize.D))
let _Qpi = ODModeSize (struct (OprMode.Q, OprSize.PI))
let _Qq = ODModeSize (struct (OprMode.Q, OprSize.Q))
let _Rd = ODModeSize (struct (OprMode.R, OprSize.D))
let _Rv = ODModeSize (struct (OprMode.R, OprSize.V))
let _Ry = ODModeSize (struct (OprMode.R, OprSize.Y))
let _SIb = ODModeSize (struct (OprMode.SI, OprSize.B))
let _SIv = ODModeSize (struct (OprMode.SI, OprSize.V))
let _SIw = ODModeSize (struct (OprMode.SI, OprSize.W))
let _SIz = ODModeSize (struct (OprMode.SI, OprSize.Z))
let _Sw = ODModeSize (struct (OprMode.S, OprSize.W))
let _Udq = ODModeSize (struct (OprMode.U, OprSize.DQ))
let _Upd = ODModeSize (struct (OprMode.U, OprSize.PD))
let _Ups = ODModeSize (struct (OprMode.U, OprSize.PS))
let _Uq = ODModeSize (struct (OprMode.U, OprSize.Q))
let _Ux = ODModeSize (struct (OprMode.U, OprSize.X))
let _Vdq = ODModeSize (struct (OprMode.V, OprSize.DQ))
let _Vpd = ODModeSize (struct (OprMode.V, OprSize.PD))
let _Vps = ODModeSize (struct (OprMode.V, OprSize.PS))
let _Vq = ODModeSize (struct (OprMode.V, OprSize.Q))
let _Vqq = ODModeSize (struct (OprMode.V, OprSize.QQ))
let _Vsd = ODModeSize (struct (OprMode.V, OprSize.SD))
let _Vss = ODModeSize (struct (OprMode.V, OprSize.SS))
let _Vx = ODModeSize (struct (OprMode.V, OprSize.X))
let _Vy = ODModeSize (struct (OprMode.V, OprSize.Y))
let _VZxz = ODModeSize (struct (OprMode.VZ, OprSize.XZ))
let _Wd = ODModeSize (struct (OprMode.W, OprSize.D))
let _Wdq = ODModeSize (struct (OprMode.W, OprSize.DQ))
let _Wdqd = ODModeSize (struct (OprMode.W, OprSize.DQD))
let _Wdqdq = ODModeSize (struct (OprMode.W, OprSize.DQDQ))
let _Wdqq = ODModeSize (struct (OprMode.W, OprSize.DQQ))
let _Wdqqdq = ODModeSize (struct (OprMode.W, OprSize.DQQDQ))
let _Wdqw = ODModeSize (struct (OprMode.W, OprSize.DQW))
let _Wdqwd = ODModeSize (struct (OprMode.W, OprSize.DQWD))
let _Wpd = ODModeSize (struct (OprMode.W, OprSize.PD))
let _Wps = ODModeSize (struct (OprMode.W, OprSize.PS))
let _Wpsq = ODModeSize (struct (OprMode.W, OprSize.PSQ))
let _Wsd = ODModeSize (struct (OprMode.W, OprSize.SD))
let _Wsdq = ODModeSize (struct (OprMode.W, OprSize.SDQ))
let _Wss = ODModeSize (struct (OprMode.W, OprSize.SS))
let _Wssd = ODModeSize (struct (OprMode.W, OprSize.SSD))
let _Wssq = ODModeSize (struct (OprMode.W, OprSize.SSQ))
let _Wx = ODModeSize (struct (OprMode.W, OprSize.X))
let _WZxz = ODModeSize (struct (OprMode.WZ, OprSize.XZ))
let _Xb = ODModeSize (struct (OprMode.X, OprSize.B))
let _Xv = ODModeSize (struct (OprMode.X, OprSize.V))
let _Yb = ODModeSize (struct (OprMode.Y, OprSize.B))
let _Yv = ODModeSize (struct (OprMode.Y, OprSize.V))

let Ap = [| _Ap |]
let Dd = [| _Dd |]
let E0v = [| _E0v |]
let Eb = [| _Eb |]
let Ep = [| _Ep |]
let Ev = [| _Ev |]
let Ew = [| _Ew |]
let Ey = [| _Ey |]
let Gb = [| _Gb |]
let Gd = [| _Gd |]
let Gv = [| _Gv |]
let Gw = [| _Gw |]
let Gy = [| _Gy |]
let Gz = [| _Gz |]
let Ib = [| _Ib |]
let Iv = [| _Iv |]
let Iw = [| _Iw |]
let Iz = [| _Iz |]
let Jb = [| _Jb |]
let Jz = [| _Jz |]
let Ma = [| _Ma |]
let Mdq = [| _Mdq |]
let Mp = [| _Mp |]
let Mq = [| _Mq |]
let Ms = [| _Ms |]
let Mv = [| _Mv |]
let Mw = [| _Mw |]
let My = [| _My |]
let Mz = [| _Mz |]
let Pd = [| _Pd |]
let Pq = [| _Pq |]
let Qq = [| _Qq |]
let Rd = [| _Rd |]
let Rv = [| _Rv |]
let Ry = [| _Ry |]
let SIb = [| _SIb |]
let SIv = [| _SIv |]
let SIw = [| _SIw |]
let SIz = [| _SIz |]
let Sw = [| _Sw |]
let Vdq = [| _Vdq |]
let Vx = [| _Vx |]
let Wdq = [| _Wdq |]
let Wdqd = [| _Wdqd |]
let Wdqq = [| _Wdqq |]
let Wx = [| _Wx |]

let ALDX = [| ODReg R.AL; ODReg R.DX |]
let ALIb = [| ODReg R.AL; _Ib |]
let ALOb = [| ODReg R.AL; _Ob |]
let BNDRbndBNDRMbnd = [| _BNDRbnd; _BNDRMbnd |]
let BNDRMbndBNDRbnd = [| _BNDRMbnd; _BNDRbnd |]
let CdRd = [| _Cd; _Rd |]
let DdRd = [| _Dd; _Rd |]
let DXAL = [| ODReg R.DX; ODReg R.AL |]
let Eb1L = [| _Eb; ODImmOne |]
let EbCL = [| _Eb; ODReg R.CL |]
let EbGb = [| _Eb; _Gb |]
let EbIb = [| _Eb; _Ib |]
let Ev1L = [| _Ev; ODImmOne |]
let EvCL = [| _Ev; ODReg R.CL |]
let EvGv = [| _Ev; _Gv |]
let EvIb = [| _Ev; _Ib |]
let EvIz = [| _Ev; _Iz |]
let EvSIb = [| _Ev; _SIb |]
let EvSIz = [| _Ev; _SIz |]
let EvSw = [| _Ev; _Sw |]
let EwGw = [| _Ew; _Gw |]
let EyPd = [| _Ey; _Pd |]
let EyPq = [| _Ey; _Pq |]
let EyVdq = [| _Ey; _Vdq |]
let GbEb = [| _Gb; _Eb |]
let GdEb = [| _Gd; _Eb |]
let GdEw = [| _Gd; _Ew |]
let GdEy = [| _Gd; _Ey |]
let GdNq = [| _Gd; _Nq |]
let GdUdq = [| _Gd; _Udq |]
let GdUx = [| _Gd; _Ux |]
let GvEb = [| _Gv; _Eb |]
let GvEd = [| _Gv; _Ed |]
let GvEv = [| _Gv; _Ev |]
let GvEw = [| _Gv; _Ew |]
let GvEy = [| _Gv; _Ey |]
let GvMa = [| _Gv; _Ma |]
let GvMp = [| _Gv; _Mp |]
let GvMv = [| _Gv; _Mv |]
let GwMw = [| _Gw; _Mw |]
let GyMy = [| _Gy; _My |]
let GyUdq = [| _Gy; _Udq |]
let GyUpd = [| _Gy; _Upd |]
let GyUps = [| _Gy; _Ups |]
let GyUx = [| _Gy; _Ux |]
let GyWdq = [| _Gy; _Wdq |]
let GyWsd = [| _Gy; _Wsd |]
let GyWsdq = [| _Gy; _Wsdq |]
let GyWss = [| _Gy; _Wss |]
let GyWssd = [| _Gy; _Wssd |]
let GzMp = [| _Gz; _Mp |]
let IbAL = [| _Ib; ODReg R.AL |]
let IwIb = [| _Iw; _Ib |]
let MdqVdq = [| _Mdq; _Vdq |]
let MpdVpd = [| _Mpd; _Vpd |]
let MpsVps = [| _Mps; _Vps |]
let MqPq = [| _Mq; _Pq |]
let MqVdq = [| _Mq; _Vdq |]
let MwGw = [| _Gw; _Mw |]
let MxVx = [| _Mx; _Vx |]
let MyGy = [| _My; _Gy |]
let MZxzVZxz = [| _MZxz; _VZxz |]
let NqIb = [| _Nq; _Ib |]
let ObAL = [| _Ob; ODReg R.AL |]
let PdEy = [| _Pd; _Ey |]
let PpiWdq = [| _Ppi; _Wdq |]
let PpiWdqq = [| _Ppi; _Wdqq |]
let PpiWpd = [| _Ppi; _Wpd |]
let PpiWps = [| _Ppi; _Wps |]
let PpiWpsq = [| _Ppi; _Wpsq |]
let PqEy = [| _Pq; _Ey |]
let PqQd = [| _Pq; _Qd |]
let PqQq = [| _Pq; _Qq |]
let PqUdq = [| _Pq; _Udq |]
let PqWdq = [| _Pq; _Wdq |]
let QpiWpd = [| _Qpi; _Wpd |]
let QqPq = [| _Qq; _Pq |]
let RdCd = [| _Rd; _Cd |]
let RdDd = [| _Rd; _Dd |]
let SwEw = [| _Sw; _Ew |]
let UdqIb = [| _Udq; _Ib |]
let VdqEdbIb = [| _Vdq; _Edb; _Ib |]
let VdqEy = [| _Vdq; _Ey |]
let VdqMdq = [| _Vdq; _Mdq |]
let VdqMq = [| _Vdq; _Mq |]
let VdqNq = [| _Vdq; _Nq |]
let VdqQq = [| _Vdq; _Qq |]
let VdqUdq = [| _Vdq; _Udq |]
let VdqWdq = [| _Vdq; _Wdq |]
let VdqWdqd = [| _Vdq; _Wdqd |]
let VdqWdqq = [| _Vdq; _Wdqq |]
let VdqWdqw = [| _Vdq; _Wdqw |]
let VpdWpd = [| _Vpd; _Wpd |]
let VpsWps = [| _Vps; _Wps |]
let VqqMdq = [| _Vqq; _Mdq |]
let VsdWsd = [| _Vsd; _Wsd |]
let VsdWsdq = [| _Vsd; _Wsdq |]
let VssWss = [| _Vss; _Wss |]
let VssWssd = [| _Vss; _Wssd |]
let VxMd = [| _Vx; _Md |]
let VxMx = [| _Vx; _Mx |]
let VxWdqdq = [| _Vx; _Wdqdq |]
let VxWdqqdq = [| _Vx; _Wdqqdq |]
let VxWdqwd = [| _Vx; _Wdqwd |]
let VxWss = [| _Vx; _Wss |]
let VxWssd = [| _Vx; _Wssd |]
let VxWssq = [| _Vx; _Wssq |]
let VxWx = [| _Vx; _Wx |]
let VyEy = [| _Vy; _Ey |]
let VZxzWdqd = [| _VZxz; _Wdqd |]
let VZxzWZxz = [| _VZxz; _WZxz |]
let WdqdVdq = [| _Wdqd; _Vdq |]
let WdqqVdq = [| _Wdqq; _Vdq |]
let WdqVdq = [| _Wdq; _Vdq |]
let WpdVpd = [| _Wpd; _Vpd |]
let WpsVps = [| _Wps; _Vps |]
let WssdVx = [| _Wssd; _Vx |]
let WssVx = [| _Wss; _Vx |]
let WxVx = [| _Wx; _Vx |]
let WZxzVZxz = [| _WZxz; _VZxz |]
let XbYb = [| _Xb; _Yb |]
let XvYv = [| _Xv; _Yv |]
let YbXb = [| _Yb; _Xb |]
let YvXv = [| _Yv; _Xv |]

let EvGvCL = [| _Ev; _Gv; ODReg R.CL |]
let EvGvIb = [| _Ev; _Gv; _Ib |]
let GdNqIb = [| _Gd; _Nq; _Ib |]
let GdUdqIb = [| _Gd; _Udq; _Ib |]
let GvEvIb = [| _Gv; _Ev; _Ib |]
let GvEvIz = [| _Gv; _Ev; _Iz |]
let GvEvSIb = [| _Gv; _Ev; _SIb |]
let GvEvSIz = [| _Gv; _Ev; _SIz |]
let GyByEy = [| _Gy; _By; _Ey |]
let GyEyBy = [| _Gy; _Ey; _By |]
let GyEyIb = [| _Gy; _Ey; _Ib |]
let HxUxIb = [| _Hx; _Ux; _Ib |]
let PqEdwIb = [| _Pq; _Edw; _Ib |]
let PqQqIb = [| _Pq; _Qq; _Ib |]
let VdqEdwIb =  [| _Vdq; _Edw; _Ib |]
let VdqHdqMdq = [| _Vdq; _Hdq; _Mdq |]
let VdqHdqMdqd = [| _Vdq; _Hdq; _Mdqd |]
let VdqHdqMq = [| _Vdq; _Hdq; _Mq |]
let VdqHdqUdq = [| _Vdq; _Hdq; _Udq |]
let VdqWdqIb = [| _Vdq; _Wdq; _Ib |]
let VpdHpdWpd = [| _Vpd; _Hpd; _Wpd |]
let VpsHpsWps = [| _Vps; _Hps; _Wps |]
let VsdHsdEy = [| _Vsd; _Hsd; _Ey |]
let VsdHsdWsd = [| _Vsd; _Hsd; _Wsd |]
let VsdHsdWsdq = [| _Vsd; _Hsd; _Wsdq |]
let VsdWsdIb = [| _Vsd; _Wsd; _Ib |]
let VsdWsdqIb = [| _Vsd; _Wsdq; _Ib |]
let VssHssEy = [| _Vss; _Hss; _Ey |]
let VssHssWss = [| _Vss; _Hss; _Wss |]
let VssHssWssd = [| _Vss; _Hss; _Wssd |]
let VssWssdIb = [| _Vss; _Wssd; _Ib |]
let VxHxWdq = [| _Vx; _Hx; _Wdq |]
let VxHxWsd = [| _Vx; _Hx; _Wsd |]
let VxHxWss = [| _Vx; _Hx; _Wss |]
let VxHxWx = [| _Vx; _Hx; _Wx |]
let VxWxIb = [| _Vx; _Wx; _Ib |]
let WsdHxVsd = [| _Wsd; _Hx; _Vsd |]
let WssHxVss = [| _Wss; _Hx; _Vss |]

let VdqHdqEdwIb = [| _Vdq; _Hdq; _Edw; _Ib |]
let VpsHpsWpsIb = [| _Vps; _Hps; _Wps; _Ib |]
let VqqHqqWdqIb = [| _Vqq; _Hqq; _Wdq; _Ib |]
let VxHxWxIb = [| _Vx; _Hx; _Wx; _Ib |]

let inline private _RGz rg changeable =
  ODRegGrp (rg, OprSize.Z, if changeable then RGrpAttr.ARegInOpREX
                           else RGrpAttr.ARegInOpNoREX)
let inline private _RGv rg changeable =
  ODRegGrp (rg, OprSize.V, if changeable then RGrpAttr.ARegInOpREX
                           else RGrpAttr.ARegInOpNoREX)

let RGzRGz = [| _RGz RegGrp.RG0 false; _RGz RegGrp.RG0 true |]
let RGvSIz = [| _RGv RegGrp.RG0 false; _SIz |]
let RGzDX = [| _RGz RegGrp.RG0 false; ODReg R.DX |]
let DXRGz = [| ODReg R.DX; _RGz RegGrp.RG0 false |]

(*
let ORSR sg = [| ODReg sg |]
let inline RegIb r = [| ODReg r; _Ib |]
let inline RGv rg = [| _RGv rg true |]
let inline RGz rg rexChangeable = [| _RGz rg rexChangeable |]
let inline RGvOv rg rc = [| _RGv rg rc; _Ov |]
let inline OvRGv rg rc = [| _Ov; _RGv rg rc |]
let inline RGvRGv rg2 = [| _RGv RegGrp.RG0 false; _RGv rg2 true |]
let inline RGvIb rg rc = [| _RGv rg rc; _Ib |]
let inline IbRGv rg rc = [| _Ib; _RGv rg rc |]
let inline RGvIv rg = [| _RGv rg true; _Iv |]
*)

/// Convert to constants
let segRegs = [| R.ES; R.CS; R.SS; R.DS; R.FS; R.GS |]

let GPRs =
  [|
    R.RAX; R.RBX; R.RCX; R.RDX; R.RSP; R.RBP; R.RSI; R.RDI; R.EAX; R.EBX; R.ECX;
    R.EDX; R.ESP; R.EBP; R.ESI; R.EDI; R.AX; R.BX; R.CX; R.DX; R.SP; R.BP; R.SI;
    R.DI; R.AL; R.BL; R.CL; R.DL; R.AH; R.BH; R.CH; R.DH; R.R8; R.R9; R.R10;
    R.R11; R.R12; R.R13; R.R14; R.R15; R.R8D; R.R9D; R.R10D; R.R11D; R.R12D;
    R.R13D; R.R14D; R.R15D; R.R8W; R.R9W; R.R10W; R.R11W; R.R12W; R.R13W;
    R.R14W; R.R15W; R.R8L; R.R9L; R.R10L; R.R11L; R.R12L; R.R13L; R.R14L;
    R.R15L; R.SPL; R.BPL; R.SIL; R.DIL; R.EIP; R.RIP; R.ST0; R.ST1; R.ST2;
    R.ST3; R.ST4; R.ST5; R.ST6; R.ST7; R.MM0; R.MM1; R.MM2; R.MM3; R.MM4; R.MM5;
    R.MM6; R.MM7; R.XMM0; R.XMM1; R.XMM2; R.XMM3; R.XMM4; R.XMM5; R.XMM6;
    R.XMM7; R.XMM8; R.XMM9; R.XMM10; R.XMM11; R.XMM12; R.XMM13; R.XMM14;
    R.XMM15; R.YMM0; R.YMM1; R.YMM2; R.YMM3; R.YMM4; R.YMM5; R.YMM6; R.YMM7;
    R.YMM8; R.YMM9; R.YMM10; R.YMM11; R.YMM12; R.YMM13; R.YMM14; R.YMM15;
    R.ZMM0; R.ZMM1; R.ZMM2; R.ZMM3; R.ZMM4; R.ZMM5; R.ZMM6; R.ZMM7; R.ZMM8;
    R.ZMM9; R.ZMM10; R.ZMM11; R.ZMM12; R.ZMM13; R.ZMM14; R.ZMM15
  |]

let registers =
  [|
    R.RAX; R.RBX; R.RCX; R.RDX; R.RSP; R.RBP; R.RSI; R.RDI; R.EAX; R.EBX; R.ECX;
    R.EDX; R.ESP; R.EBP; R.ESI; R.EDI; R.AX; R.BX; R.CX; R.DX; R.SP; R.BP; R.SI;
    R.DI; R.AL; R.BL; R.CL; R.DL; R.AH; R.BH; R.CH; R.DH; R.R8; R.R9; R.R10;
    R.R11; R.R12; R.R13; R.R14; R.R15; R.R8D; R.R9D; R.R10D; R.R11D; R.R12D;
    R.R13D; R.R14D; R.R15D; R.R8W; R.R9W; R.R10W; R.R11W; R.R12W; R.R13W;
    R.R14W; R.R15W; R.R8L; R.R9L; R.R10L; R.R11L; R.R12L; R.R13L; R.R14L;
    R.R15L; R.SPL; R.BPL; R.SIL; R.DIL; R.EIP; R.RIP; R.ST0; R.ST1; R.ST2;
    R.ST3; R.ST4; R.ST5; R.ST6; R.ST7; R.MM0; R.MM1; R.MM2; R.MM3; R.MM4; R.MM5;
    R.MM6; R.MM7; R.XMM0; R.XMM1; R.XMM2; R.XMM3; R.XMM4; R.XMM5; R.XMM6;
    R.XMM7; R.XMM8; R.XMM9; R.XMM10; R.XMM11; R.XMM12; R.XMM13; R.XMM14;
    R.XMM15; R.YMM0; R.YMM1; R.YMM2; R.YMM3; R.YMM4; R.YMM5; R.YMM6; R.YMM7;
    R.YMM8; R.YMM9; R.YMM10; R.YMM11; R.YMM12; R.YMM13; R.YMM14; R.YMM15;
    R.ZMM0; R.ZMM1; R.ZMM2; R.ZMM3; R.ZMM4; R.ZMM5; R.ZMM6; R.ZMM7; R.ZMM8;
    R.ZMM9; R.ZMM10; R.ZMM11; R.ZMM12; R.ZMM13; R.ZMM14; R.ZMM15; R.ES; R.CS;
    R.SS; R.DS; R.FS; R.GS; R.ESBase; R.CSBase; R.SSBase; R.DSBase; R.FSBase;
    R.GSBase; R.CR0; R.CR2; R.CR3; R.CR4; R.DR0; R.DR1; R.DR2; R.DR3; R.DR6;
    R.DR7; R.BND0; R.BND1; R.BND2; R.BND3; R.OF; R.DF; R.IF; R.TF; R.SF; R.ZF;
    R.AF; R.PF; R.CF; R.FCW; R.FSW; R.FTW; R.FOP; R.FIP; R.FCS; R.FDP; R.FDS;
    R.MXCSR; R.MXCSRMASK
  |]

let regGrps = [| RegGrp.RG0; RegGrp.RG1; RegGrp.RG2; RegGrp.RG3;
                 RegGrp.RG4; RegGrp.RG5; RegGrp.RG6; RegGrp.RG7 |]

let boolToStr bool = if bool then "T" else "F"

let ORSR =
  Array.map (fun r -> ("OR" + r.ToString(), [| ODReg r |])) segRegs
  |> Array.toList

let RegIb =
  Array.map (fun r -> (r.ToString() + "Ib", [| ODReg r; _Ib |])) GPRs
  |> Array.toList

let RGv isChange =
  Array.map (fun r -> ("Gv" + r.ToString().Substring(1) + boolToStr isChange,
                       [| _RGv r isChange |])) regGrps
  |> Array.toList

let rgvT = RGv true
let rgvF = RGv false
let rgv = List.append rgvT rgvF

let RGz isChange =
  Array.map (fun r -> ("Gz" + r.ToString().Substring(1) + boolToStr isChange,
                       [| _RGz r isChange |])) regGrps
  |> Array.toList

let RGvOv =
  rgv |> List.map (fun (name, rgv) -> (name + "Ov", [| rgv.[0]; _Ov |]))

let OvRGv =
  rgv |> List.map (fun (name, rgv) -> ("Ov" + name, [| _Ov; rgv.[0] |]))

let RGvRGv =
  let (r1n, r1e) = rgvF.[0]
  rgvT |> List.map (fun (name, rgv) -> (r1n + name, [| r1e.[0]; rgv.[0] |]))

let RGvIb =
  rgv |> List.map (fun (name, rgv) -> (name + "Ib", [| rgv.[0]; _Ib |]))

let IbRGv =
  rgv |> List.map (fun (name, rgv) -> ("Ib" + name, [| _Ib; rgv.[0] |]))

let RGvIv =
  rgv |> List.map (fun (name, rgv) -> (name + "Iv", [| rgv.[0]; _Iv |]))

let descWithParam =
  ORSR @ (* RegIb @ *) rgvT @ RGz true @ RGz false @ RGvOv @ OvRGv @ RGvRGv @
  RGvIb @ IbRGv @ RGvIv

let oprModeSize =
  [
    ("_Ib", ODModeSize (struct (OprMode.I, OprSize.B)))
    ("_SIb", ODModeSize (struct (OprMode.SI, OprSize.B)))
    ("_SIz", ODModeSize (struct (OprMode.SI, OprSize.Z)))
  ]

let descs =
  [
    ("Ap", [| _Ap |])
    ("Dd", [| _Dd |])
    ("E0v", [| _E0v |])
    ("Eb", [| _Eb |])
    ("Ep", [| _Ep |])
    ("Ev", [| _Ev |])
    ("Ew", [| _Ew |])
    ("Ey", [| _Ey |])
    ("Gb", [| _Gb |])
    ("Gd", [| _Gd |])
    ("Gv", [| _Gv |])
    ("Gw", [| _Gw |])
    ("Gy", [| _Gy |])
    ("Gz", [| _Gz |])
    ("Ib", [| _Ib |])
    ("Iv", [| _Iv |])
    ("Iw", [| _Iw |])
    ("Iz", [| _Iz |])
    ("Jb", [| _Jb |])
    ("Jz", [| _Jz |])
    ("Ma", [| _Ma |])
    ("Mdq", [| _Mdq |])
    ("Mp", [| _Mp |])
    ("Mq", [| _Mq |])
    ("Ms", [| _Ms |])
    ("Mv", [| _Mv |])
    ("Mw", [| _Mw |])
    ("My", [| _My |])
    ("Mz", [| _Mz |])
    ("Pd", [| _Pd |])
    ("Pq", [| _Pq |])
    ("Qq", [| _Qq |])
    ("Rd", [| _Rd |])
    ("Rv", [| _Rv |])
    ("Ry", [| _Ry |])
    ("SIb", [| _SIb |])
    ("SIv", [| _SIv |])
    ("SIw", [| _SIw |])
    ("SIz", [| _SIz |])
    ("Sw", [| _Sw |])
    ("Vdq", [| _Vdq |])
    ("Vx", [| _Vx |])
    ("Wdq", [| _Wdq |])
    ("Wdqd", [| _Wdqd |])
    ("Wdqq", [| _Wdqq |])
    ("Wx", [| _Wx |])

    ("ALDX", [| ODReg R.AL; ODReg R.DX |])
    ("ALIb", [| ODReg R.AL; _Ib |])
    ("ALOb", [| ODReg R.AL; _Ob |])
    ("BNDRbndBNDRMbnd", [| _BNDRbnd; _BNDRMbnd |])
    ("BNDRMbndBNDRbnd", [| _BNDRMbnd; _BNDRbnd |])
    ("CdRd", [| _Cd; _Rd |])
    ("DdRd", [| _Dd; _Rd |])
    ("DXAL", [| ODReg R.DX; ODReg R.AL |])
    ("Eb1L", [| _Eb; ODImmOne |])
    ("EbCL", [| _Eb; ODReg R.CL |])
    ("EbGb", [| _Eb; _Gb |])
    ("EbIb", [| _Eb; _Ib |])
    ("Ev1L", [| _Ev; ODImmOne |])
    ("EvCL", [| _Ev; ODReg R.CL |])
    ("EvGv", [| _Ev; _Gv |])
    ("EvIb", [| _Ev; _Ib |])
    ("EvIz", [| _Ev; _Iz |])
    ("EvSIb", [| _Ev; _SIb |])
    ("EvSIz", [| _Ev; _SIz |])
    ("EvSw", [| _Ev; _Sw |])
    ("EwGw", [| _Ew; _Gw |])
    ("EyPd", [| _Ey; _Pd |])
    ("EyPq", [| _Ey; _Pq |])
    ("EyVdq", [| _Ey; _Vdq |])
    ("GbEb", [| _Gb; _Eb |])
    ("GdEb", [| _Gd; _Eb |])
    ("GdEw", [| _Gd; _Ew |])
    ("GdEy", [| _Gd; _Ey |])
    ("GdNq", [| _Gd; _Nq |])
    ("GdUdq", [| _Gd; _Udq |])
    ("GdUx", [| _Gd; _Ux |])
    ("GvEb", [| _Gv; _Eb |])
    ("GvEd", [| _Gv; _Ed |])
    ("GvEv", [| _Gv; _Ev |])
    ("GvEw", [| _Gv; _Ew |])
    ("GvEy", [| _Gv; _Ey |])
    ("GvMa", [| _Gv; _Ma |])
    ("GvMp", [| _Gv; _Mp |])
    ("GvMv", [| _Gv; _Mv |])
    ("GwMw", [| _Gw; _Mw |])
    ("GyMy", [| _Gy; _My |])
    ("GyUdq", [| _Gy; _Udq |])
    ("GyUpd", [| _Gy; _Upd |])
    ("GyUps", [| _Gy; _Ups |])
    ("GyUx", [| _Gy; _Ux |])
    ("GyWdq", [| _Gy; _Wdq |])
    ("GyWsd", [| _Gy; _Wsd |])
    ("GyWsdq", [| _Gy; _Wsdq |])
    ("GyWss", [| _Gy; _Wss |])
    ("GyWssd", [| _Gy; _Wssd |])
    ("GzMp", [| _Gz; _Mp |])
    ("IbAL", [| _Ib; ODReg R.AL |])
    ("IwIb", [| _Iw; _Ib |])
    ("MdqVdq", [| _Mdq; _Vdq |])
    ("MpdVpd", [| _Mpd; _Vpd |])
    ("MpsVps", [| _Mps; _Vps |])
    ("MqPq", [| _Mq; _Pq |])
    ("MqVdq", [| _Mq; _Vdq |])
    ("MwGw", [| _Gw; _Mw |])
    ("MxVx", [| _Mx; _Vx |])
    ("MyGy", [| _My; _Gy |])
    ("MZxzVZxz", [| _MZxz; _VZxz |])
    ("NqIb", [| _Nq; _Ib |])
    ("ObAL", [| _Ob; ODReg R.AL |])
    ("PdEy", [| _Pd; _Ey |])
    ("PpiWdq", [| _Ppi; _Wdq |])
    ("PpiWdqq", [| _Ppi; _Wdqq |])
    ("PpiWpd", [| _Ppi; _Wpd |])
    ("PpiWps", [| _Ppi; _Wps |])
    ("PpiWpsq", [| _Ppi; _Wpsq |])
    ("PqEy", [| _Pq; _Ey |])
    ("PqQd", [| _Pq; _Qd |])
    ("PqQq", [| _Pq; _Qq |])
    ("PqUdq", [| _Pq; _Udq |])
    ("PqWdq", [| _Pq; _Wdq |])
    ("QpiWpd", [| _Qpi; _Wpd |])
    ("QqPq", [| _Qq; _Pq |])
    ("RdCd", [| _Rd; _Cd |])
    ("RdDd", [| _Rd; _Dd |])
    ("SwEw", [| _Sw; _Ew |])
    ("UdqIb", [| _Udq; _Ib |])
    ("VdqEdbIb", [| _Vdq; _Edb; _Ib |])
    ("VdqEy", [| _Vdq; _Ey |])
    ("VdqMdq", [| _Vdq; _Mdq |])
    ("VdqMq", [| _Vdq; _Mq |])
    ("VdqNq", [| _Vdq; _Nq |])
    ("VdqQq", [| _Vdq; _Qq |])
    ("VdqUdq", [| _Vdq; _Udq |])
    ("VdqWdq", [| _Vdq; _Wdq |])
    ("VdqWdqd", [| _Vdq; _Wdqd |])
    ("VdqWdqq", [| _Vdq; _Wdqq |])
    ("VdqWdqw", [| _Vdq; _Wdqw |])
    ("VpdWpd", [| _Vpd; _Wpd |])
    ("VpsWps", [| _Vps; _Wps |])
    ("VqqMdq", [| _Vqq; _Mdq |])
    ("VsdWsd", [| _Vsd; _Wsd |])
    ("VsdWsdq", [| _Vsd; _Wsdq |])
    ("VssWss", [| _Vss; _Wss |])
    ("VssWssd", [| _Vss; _Wssd |])
    ("VxMd", [| _Vx; _Md |])
    ("VxMx", [| _Vx; _Mx |])
    ("VxWdqdq", [| _Vx; _Wdqdq |])
    ("VxWdqqdq", [| _Vx; _Wdqqdq |])
    ("VxWdqwd", [| _Vx; _Wdqwd |])
    ("VxWss", [| _Vx; _Wss |])
    ("VxWssd", [| _Vx; _Wssd |])
    ("VxWssq", [| _Vx; _Wssq |])
    ("VxWx", [| _Vx; _Wx |])
    ("VyEy", [| _Vy; _Ey |])
    ("VZxzWdqd", [| _VZxz; _Wdqd |])
    ("VZxzWZxz", [| _VZxz; _WZxz |])
    ("WdqdVdq", [| _Wdqd; _Vdq |])
    ("WdqqVdq", [| _Wdqq; _Vdq |])
    ("WdqVdq", [| _Wdq; _Vdq |])
    ("WpdVpd", [| _Wpd; _Vpd |])
    ("WpsVps", [| _Wps; _Vps |])
    ("WssdVx", [| _Wssd; _Vx |])
    ("WssVx", [| _Wss; _Vx |])
    ("WxVx", [| _Wx; _Vx |])
    ("WZxzVZxz", [| _WZxz; _VZxz |])
    ("XbYb", [| _Xb; _Yb |])
    ("XvYv", [| _Xv; _Yv |])
    ("YbXb", [| _Yb; _Xb |])
    ("YvXv", [| _Yv; _Xv |])

    ("EvGvCL", [| _Ev; _Gv; ODReg R.CL |])
    ("EvGvIb", [| _Ev; _Gv; _Ib |])
    ("GdNqIb", [| _Gd; _Nq; _Ib |])
    ("GdUdqIb", [| _Gd; _Udq; _Ib |])
    ("GvEvIb", [| _Gv; _Ev; _Ib |])
    ("GvEvIz", [| _Gv; _Ev; _Iz |])
    ("GvEvSIb", [| _Gv; _Ev; _SIb |])
    ("GvEvSIz", [| _Gv; _Ev; _SIz |])
    ("GyByEy", [| _Gy; _By; _Ey |])
    ("GyEyBy", [| _Gy; _Ey; _By |])
    ("GyEyIb", [| _Gy; _Ey; _Ib |])
    ("HxUxIb", [| _Hx; _Ux; _Ib |])
    ("PqEdwIb", [| _Pq; _Edw; _Ib |])
    ("PqQqIb", [| _Pq; _Qq; _Ib |])
    ("VdqEdwIb", [| _Vdq; _Edw; _Ib |])
    ("VdqHdqMdq", [| _Vdq; _Hdq; _Mdq |])
    ("VdqHdqMdqd", [| _Vdq; _Hdq; _Mdqd |])
    ("VdqHdqMq", [| _Vdq; _Hdq; _Mq |])
    ("VdqHdqUdq", [| _Vdq; _Hdq; _Udq |])
    ("VdqWdqIb", [| _Vdq; _Wdq; _Ib |])
    ("VpdHpdWpd", [| _Vpd; _Hpd; _Wpd |])
    ("VpsHpsWps", [| _Vps; _Hps; _Wps |])
    ("VsdHsdEy", [| _Vsd; _Hsd; _Ey |])
    ("VsdHsdWsd", [| _Vsd; _Hsd; _Wsd |])
    ("VsdHsdWsdq", [| _Vsd; _Hsd; _Wsdq |])
    ("VsdWsdIb", [| _Vsd; _Wsd; _Ib |])
    ("VsdWsdqIb", [| _Vsd; _Wsdq; _Ib |])
    ("VssHssEy", [| _Vss; _Hss; _Ey |])
    ("VssHssWss", [| _Vss; _Hss; _Wss |])
    ("VssHssWssd", [| _Vss; _Hss; _Wssd |])
    ("VssWssdIb", [| _Vss; _Wssd; _Ib |])
    ("VxHxWdq", [| _Vx; _Hx; _Wdq |])
    ("VxHxWsd", [| _Vx; _Hx; _Wsd |])
    ("VxHxWss", [| _Vx; _Hx; _Wss |])
    ("VxHxWx", [| _Vx; _Hx; _Wx |])
    ("VxWxIb", [| _Vx; _Wx; _Ib |])
    ("WsdHxVsd", [| _Wsd; _Hx; _Vsd |])
    ("WssHxVss", [| _Wss; _Hx; _Vss |])

    ("VdqHdqEdwIb", [| _Vdq; _Hdq; _Edw; _Ib |])
    ("VpsHpsWpsIb", [| _Vps; _Hps; _Wps; _Ib |])
    ("VqqHqqWdqIb", [| _Vqq; _Hqq; _Wdq; _Ib |])
    ("VxHxWxIb", [| _Vx; _Hx; _Wx; _Ib |])

    ("RGzRGz", [| ODRegGrp (RegGrp.RG0, OprSize.Z, RGrpAttr.ARegInOpNoREX);
                  ODRegGrp (RegGrp.RG0, OprSize.Z, RGrpAttr.ARegInOpREX) |])
    ("RGvSIz", [| ODRegGrp (RegGrp.RG0, OprSize.V, RGrpAttr.ARegInOpNoREX);
                  _SIz |])
    ("RGzDX", [| ODRegGrp (RegGrp.RG0, OprSize.Z, RGrpAttr.ARegInOpNoREX);
                 ODReg R.DX |])
    ("DXRGz", [| ODReg R.DX;
                 ODRegGrp (RegGrp.RG0, OprSize.Z, RGrpAttr.ARegInOpNoREX) |])
  ]

let toInt64 = function
  | ODImmOne -> (1L <<< 12)
  | ODModeSize (struct (mode, sz)) ->
      let sz: int64 = LanguagePrimitives.EnumToValue sz |> int64
      let mode: int64 = LanguagePrimitives.EnumToValue mode |> int64
      (2L <<< 12) ||| sz ||| mode
  | ODReg reg ->
      let reg: int64 = LanguagePrimitives.EnumToValue reg |> int64
      (3L <<< 12) ||| reg
  | ODRegGrp (regGrp, oprSize, rGrpAttr) ->
      let oprSize: int64 = LanguagePrimitives.EnumToValue oprSize |> int64
      let regGrp: int64 = LanguagePrimitives.EnumToValue regGrp |> int64
      let rGrpAttr: int64 = LanguagePrimitives.EnumToValue rGrpAttr |> int64
      (4L <<< 12) ||| oprSize ||| (regGrp <<< 3) ||| rGrpAttr

let combineDescs descs =
  descs
  |> Array.mapi (fun idx desc -> desc <<< (48 - idx * 16))
  |> Array.fold (fun acc desc -> desc ||| acc) 0L

let main _args =
  oprModeSize
  |> List.iter (fun (var, desc) ->
       printfn "let [<Literal>] %s = 0x%xL" var (toInt64 desc))

  descs
  |> List.iter (fun (var, descs) ->
       printfn "let [<Literal>] %s = 0x%xL"
               var (Array.map toInt64 descs |> combineDescs))

  descWithParam
  |> List.iter (fun (var, descs) ->
       printfn "let [<Literal>] %s = 0x%xL"
               var (Array.map toInt64 descs |> combineDescs))

fsi.CommandLineArgs |> main
