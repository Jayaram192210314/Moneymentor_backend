# --------------------------------------------------
# GOLD SCRAPER WITH LAST 10 DAYS TABLE
# --------------------------------------------------
def get_gold_price(place="chennai"):

    place = place.lower().strip()
    url_gold = f"https://www.goodreturns.in/gold-rates/{place}.html"

    scraper = cloudscraper.create_scraper()

    try:
        gold_response = scraper.get(url_gold)
        if gold_response.status_code != 200:
            return None, f"Failed with status {gold_response.status_code}"

        soup_gold = BeautifulSoup(gold_response.text, "html.parser")

        # 24K Price Today
        price_24k_element = soup_gold.find("span", id="24K-price")
        if not price_24k_element:
            return None, "24K price not found"

        price_24k = price_24k_element.text.strip().replace("₹", "").replace(",", "")

        # Extract last 10 days table
        last10_json = []
        tables = soup_gold.find_all("table")

        target_table = None
        for tbl in tables:
            headers = [th.get_text(strip=True).lower() for th in tbl.find_all("th")]
            if any("24" in h for h in headers) and any("22" in h for h in headers):
                target_table = tbl
                break

        if not target_table:
            return {"24K": price_24k, "table": []}, None

        rows = target_table.find("tbody").find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            date = cols[0].get_text(strip=True)

            # 24K
            col_24k_raw = cols[1].get_text(" ", strip=True).replace("₹", "").replace(",", "")
            p24 = col_24k_raw.split()
            price_24k_day = p24[0]
            change_24k_day = p24[1].strip("()") if len(p24) > 1 else "0"

            # 22K
            col_22k_raw = cols[2].get_text(" ", strip=True).replace("₹", "").replace(",", "")
            p22 = col_22k_raw.split()
            price_22k_day = p22[0]
            change_22k_day = p22[1].strip("()") if len(p22) > 1 else "0"

            last10_json.append({
                "date": date,
                "24k": price_24k_day,
                "24k_change": change_24k_day,
                "22k": price_22k_day,
                "22k_change": change_22k_day
            })

        return {
            "24K": price_24k,
            "table": last10_json
        }, None

    except Exception as e:
        return None, str(e)



# --------------------------------------------------
# GOLD GRAPH (STATIC PNG) – WITH FIXED DATE LABELS
# --------------------------------------------------
def generate_gold_graph(table_data):

    if not table_data:
        return None

    # ----- FIXED DATE PARSING -----
    dates = []
    for row in table_data:
        try:
            d = datetime.strptime(row["date"], "%b %d, %Y")
            dates.append(d.strftime("%d %b"))  # Example: 20 Feb
        except:
            dates.append(row["date"])

    dates = dates[::-1]  # oldest → latest

    prices_24k = [int(row["24k"]) for row in table_data][::-1]
    prices_22k = [int(row["22k"]) for row in table_data][::-1]

    x = np.arange(len(dates))

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 5), dpi=140)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # GOLD COLORS
    gold_light = "#FFF4D6"   # Soft gold highlight
    gold_mid   = "#F2C94C"   # Smooth bright gold
    gold_dark  = "#B8860B"   # Deep metallic gold
    gold_dark2 = "#D4A017"   # Polished royal gold
    # Smooth Lines
    ax.plot(x, prices_24k, color=gold_dark, linewidth=3)
    ax.plot(x, prices_22k, color=gold_dark2, linewidth=3)

    # Golden gradient area
    ax.fill_between(x, prices_24k, color=gold_mid, alpha=0.35)
    ax.fill_between(x, prices_22k, color=gold_light, alpha=0.35)

    # Clean grid
    ax.grid(color="#e0d8c3", linestyle="--", linewidth=0.7, alpha=0.7)

    # Remove border lines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # X-axis labels (Fixed)
    ax.set_xticks(x)
    ax.set_xticklabels(dates, fontsize=10, color="#333")

    # Legend
    ax.legend(
        ["24K Gold", "22K Gold"],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=2,
        frameon=False,
        fontsize=11
    )

    plt.tight_layout()

    # Output PNG
    img = BytesIO()
    plt.savefig(img, format="png", bbox_inches="tight")
    img.seek(0)
    plt.close()

    return img



# --------------------------------------------------
# GOLD JSON API
# --------------------------------------------------
@app.route("/gold", methods=["GET"])
def gold_rate():

    place = request.args.get("place", "chennai")
    prices, error = get_gold_price(place)

    if error:
        return jsonify({"status": "error", "message": error}), 400

    table = prices["table"]
    today = table[0] if len(table) > 0 else {}

    return jsonify({
        "status": "success",
        "place": place,
        "gold_price_24k_per_gram": prices["24K"],
        "gold_price_22k_per_gram": today.get("22k", "NA"),
        "change_24k_today": today.get("24k_change", "0"),
        "change_22k_today": today.get("22k_change", "0"),
        "currency": "INR",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })



# --------------------------------------------------
# GOLD GRAPH API
# --------------------------------------------------
@app.route("/gold-graph", methods=["GET"])
def gold_graph():

    place = request.args.get("place", "chennai")
    prices, error = get_gold_price(place)

    if error:
        return jsonify({"status": "error", "message": error}), 400

    img = generate_gold_graph(prices["table"])

    return send_file(
        img,
        mimetype="image/png",
        as_attachment=False,
        download_name="gold_graph.png"
    )