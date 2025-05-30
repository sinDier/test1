from flask import Flask, request, jsonify
from flask_cors import CORS  
import math

app = Flask(__name__)
CORS(app) 


m_e = 9.10938356e-31  
c = 3e8                

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
       
        data = request.get_json()
        v_frac = float(data['velocity'])

        if not 0 <= v_frac <= 1:
            raise ValueError("速度必须在0到1之间")

        v = v_frac * c

       
        classical_ke = 0.5 * m_e * v**2
        classical_p = m_e * v

      
        gamma = 1 / math.sqrt(1 - (v_frac**2))
        relativistic_ke = (gamma - 1) * m_e * c**2
        relativistic_p = gamma * m_e * v

      
        speeds = [i/100 for i in range(1, 100)]
        classic_k = [0.5 * m_e * (s*c)**2 for s in speeds]
        relativ_k = [(1/math.sqrt(1-s**2)-1)*m_e*c**2 for s in speeds]
        classic_p = [m_e * s*c for s in speeds]
        relativ_p = [m_e*s*c/math.sqrt(1-s**2) for s in speeds]

        return jsonify({
            'speeds': speeds,
            'classic_k': classic_k,      
            'relativ_k': relativ_k,
            'classic_p': classic_p,
            'relativ_p': relativ_p,
            'classical_ke': classical_ke,
            'relativistic_ke': relativistic_ke,
            'classical_p': classical_p,
            'relativistic_p': relativistic_p
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)