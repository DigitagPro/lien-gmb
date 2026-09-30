// Fonction serverless (Vercel) : la clé SerpAPI reste côté serveur.
// Variable d'environnement à créer sur Vercel : SERPAPI_KEY

export default async function handler(req, res) {
  const q = (req.query.q || "").toString().trim();
  if (!q) {
    return res.status(400).json({ error: "Requête vide." });
  }

  const key = process.env.SERPAPI_KEY;
  if (!key) {
    return res.status(500).json({ error: "Clé SERPAPI_KEY non configurée sur le serveur." });
  }

  const url =
    "https://serpapi.com/search.json?engine=google_maps&type=search&hl=fr&q=" +
    encodeURIComponent(q) +
    "&api_key=" +
    encodeURIComponent(key);

  try {
    const r = await fetch(url);
    const data = await r.json();

    if (data.error) {
      return res.status(502).json({ error: data.error });
    }

    const raw = data.local_results || (data.place_results ? [data.place_results] : []);
    const results = raw
      .filter((p) => p.place_id)
      .map((p) => ({
        title: p.title,
        address: p.address || "",
        place_id: p.place_id,
      }));

    res.setHeader("Cache-Control", "s-maxage=3600, stale-while-revalidate");
    return res.status(200).json({ results });
  } catch (e) {
    return res.status(500).json({ error: "Erreur serveur : " + e.message });
  }
}
