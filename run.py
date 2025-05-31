from app import create_app

app = create_app()


if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(f"[FLASK] {rule.rule} [{','.join(sorted(rule.methods))}] --> {rule.endpoint}:") 
    app.run(debug=True, port=3000)