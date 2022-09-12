from flask import Flask, request
app = Flask(__name__)

@app.route('/api', methods=['GET'])
def load_html():
    comuna_id = request.args.get('com_id')
    person_id = request.args.get('p_id')

    if not check_valid_comuna(comuna_id):
        return "You give an invalid comuna id, please sue the correct ones."
    
    region, comuna = get_region_comuna_names(comuna_id)
    response_data = get_hallazgos(comuna_id)
    if not response_data:
        return "An error has ocurred calling the API, please reload the page again."
    
    summary_table, pie_chart = generate_table(response_data)
    body_table = build_table_body(summary_table)
    chart_script = build_chart_script(pie_chart)
    html = get_page()
    return html.format(region_name=region.lower(), comuna_name=comuna.lower(), table_body=body_table, chart_script=chart_script)

if __name__ == '__main__':
    import bjoern
    bjoern.run(app, "0.0.0.0", 8094)
