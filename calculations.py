from flask import Flask, request, jsonify
import math

app = Flask(__name__)

con = 0.00000001

@app.route('/calculate-source', methods=['POST'])
def calculate_source():
    data = request.get_json()
    Ta = data['ambientTemp']
    l = data['length']
    b = data['breadth']
    t = data['thickness']
    k = data['k']
    power = data['power']
    
    ep = 0.85
    a = l * b
    A1 = (t * power) / (k * a)
    A2 = (1.32 * t) / (k * l ** 0.25)
    A3 = (ep * t * 5.67 * 10 ** -8) / k
    A4 = (1.32 * a) / (l ** 0.25)
    A5 = 5.67 * 10 ** -8 * a * ep
    A6 = (0.59 * a) / (l ** 0.25)

    def fun(Ts):
        Tb = (Ts - A1 + (A2) * (Ts - Ta) ** 1.25) + ((A3) * (Ts ** 4 - Ta ** 4))
        p = ((A4 * (Ts - Ta) ** 1.25) + (A5 * (Ts ** 4 + Tb ** 4 - 2 * Ta ** 4)) + (A6 * (Tb - Ta) ** 1.25)) - power
        return p

    def fundev(Ts):
        Tb = (Ts - A1 + A2 * (Ts - Ta) ** 1.25) + (A3 * (Ts ** 4 - Ta ** 4))
        Tbdash = (1 - (1.25 * A2 * (Ts - Ta) ** 0.25) + (4 * A3 * Ts ** 3))
        q = (1.25 * A4 * (Ts - Ta) ** 0.25) + (A5 * Ts ** 3 * 4) + (1.25 * A6 * (Tb - Ta) ** 0.25 * Tbdash) + (4 * A5 * Tb ** 3 * Tbdash)
        return q

    def newtonraphson(iniTs):
        Ts = iniTs
        h = fun(Ts) / fundev(Ts)
        while abs(h) >= con:
            h = fun(Ts) / fundev(Ts)
            Ts = Ts - h
        return Ts

    iniTs = 350.0
    Ts = newtonraphson(iniTs)
    
    return jsonify({'temperature': Ts})

@app.route('/calculate-ambient', methods=['POST'])
def calculate_ambient():
    data = request.get_json()
    Ts = data['sourceTemp']
    l = data['length']
    b = data['breadth']
    t = data['thickness']
    k = data['k']
    power = data['power']
    
    ep = 0.85
    a = l * b
    A1 = (t * power) / (k * a)
    A2 = (1.32 * t) / (k * l ** 0.25)
    A3 = (ep * t * 5.67 * 10 ** -8) / k
    A4 = (1.32 * a) / (l ** 0.25)
    A5 = 5.67 * 10 ** -8 * a * ep
    A6 = (0.59 * a) / (l ** 0.25)

    def fun(Ta):
        Tb = (Ts - A1 + (A2) * (Ts - Ta) ** 1.25) + ((A3) * (Ts ** 4 - Ta ** 4))
        p = ((A4 * (Ts - Ta) ** 1.25) + (A5 * (Ts ** 4 + Tb ** 4 - 2 * Ta ** 4)) + (A6 * (Tb - Ta) ** 1.25)) - power
        return p

    def fundev(Ta):
        Tb = (Ts - A1 + A2 * (Ts - Ta) ** 1.25) + (A3 * (Ts ** 4 - Ta ** 4))
        Tbdash = (0 - (1.25 * A2 * (Ts - Ta) ** 0.25) - (4 * A3 * Ta ** 3))
        q = (-1.25 * A4 * (Ts - Ta) ** 0.25) + (-A5 * 2 * Ta ** 3 * 4) + (-1.25 * A6 * (Tb - Ta) ** 0.25 * Tbdash) + (4 * A5 * Tb ** 3 * Tbdash)
        return q

    def newtonraphson(iniTa):
        Ta = iniTa
        h = fun(Ta) / fundev(Ta)
        while abs(h) >= con:
            h = fun(Ta) / fundev(Ta)
            Ta = Ta - h
        return Ta

    iniTa = 350.0
    Ta = newtonraphson(iniTa)
    
    return jsonify({'temperature': Ta})

if __name__ == '__main__':
    app.run(debug=True)
