# ikea-product-names

### *Can the famous IKEA product names tell us what category they belong to?*

This project, by **Jonathan Jayes**, explores whether the unique naming conventions of IKEA products can be leveraged to predict their product category. By converting product names into numerical representations (text embeddings), we can build a machine learning model that finds patterns and improves classification accuracy compared to a baseline model.

## What's in a Name? The IKEA Naming System

IKEA is known for its distinctive product names, which are not random but follow a specific internal logic. The naming system often draws from Scandinavian languages, using words for places, names, plants, and more to denote different types of products. This underlying structure is the key that this project aims to unlock.

For example, sofas are often named after Swedish places, while rugs get their names from Danish locales.

Here's a glimpse into the system:

| Product Category | Naming Rule | Examples |
| :--- | :--- | :--- |
| Upholstered furniture, Sofas, Armchairs | Swedish place names (toponyms) | KLIPPAN, EKTORP, SÖDERHAMN |
| Bookcases / Bookshelf series | Professions, Scandinavian boy's names | BILLY, KALLAX, HEMNES |
| Beds, Wardrobes, Hall furniture | Norwegian place names | HEMNES, MALM, MANDAL |
| Dining tables and chairs | Finnish & Swedish place names | BJURSTA, INGATORP, DOCKSTA |
| Bathroom articles & storage | Scandinavian/Swedish lakes, rivers, bays | BOLMEN, TOFTAN, VOXNAN |
| Outdoor/Garden furniture | Scandinavian/Swedish islands | ÄPPLARÖ, SOLLERON, MASTHOLMEN |
| Children's articles | Mammals, birds, adjectives (Swedish) | DUKTIG, KRITTER, BLÅHAJ |
| Bed textiles/linen, covers, pillows | Flowers, plants, precious stones | ULLVIDE, NATTJASMIN, STENKLÖVER |
| Carpets / Rugs | Danish place names | ÅDUM, VEMB, KATTRUP |
| Lighting products | Units, seasons, months, nautical terms | ÅRSTID, HEKTAR, NYMÅNE |

## 🧐 Research Question

**Can we use the naming conventions of IKEA products, captured via text embeddings, to accurately predict the category of a product?**

## ⚙️ Project Pipeline

The project followed a clear, multi-step process to answer the research question.

### Step 1: Data Collection

First, a web scraper was built to gather data directly from the IKEA website. The scraper collected key variables for a range of furniture products.

**Variables Collected:**

  - `product_name`: The unique name of the product (e.g., "BILLY").
  - `product_category`: The target variable for prediction (e.g., "Bookcases & shelving units").
  - `short_description`: A brief text description.
  - `price`: The retail price.
  - `dimensions`: Product dimensions (L, W, H).
  - `other_colours`: A flag for availability in other colors.


### Step 2: Baseline Model

A baseline classification model was created using the scraped data *without* considering the product names. This provides a benchmark to measure our improvements against.

The baseline model achieved a **weighted average F1-score of 0.54**. The performance varied significantly across categories, with some (like "Trolleys") being easier to predict than others (like "Café furniture" or "Room dividers").

### Step 3: Introducing Text Embeddings

This is where the product names come into play. A **text embedding** is a technique to represent words or phrases as dense vectors of numbers. This allows a machine learning model to "understand" the relationships and semantic similarities between different names.

Since these embedding vectors can be very large, **Uniform Manifold Approximation and Projection (UMAP)** was used to reduce their dimensionality, making them easier for the model to process while retaining the most important information.

### Step 4: Improved Prediction with Embeddings

The UMAP components derived from the product name embeddings were added as features to the dataset. A new classification model was then trained on this enriched data.

The results showed a clear improvement. The new model achieved a **weighted average F1-score of 0.60**, a significant lift from the baseline's 0.54.

## 📊 Findings

The addition of text embedding features improved precision and recall for several key categories. To ensure these new UMAP features were genuinely contributing, a feature importance analysis was performed. The results confirm that the embedding features (e.g., `UMAP_1`, `UMAP_2`) were among the influential variables in the model's decisions.

## ✅ Takeaways

  - The systematic naming conventions of IKEA products are not just a branding quirk; they contain a **meaningful signal** that can be used for product categorization.
  - **Text embeddings** are a powerful tool for converting unstructured text data, like product names, into valuable features for machine learning models.
  - The F1-score improvement from **54% to 60%** demonstrates that including name embeddings significantly enhances classification performance over a model that relies on other product attributes alone.