# Active l'environnement virtuel
echo "Activating Python virtual environment..."
source ~/Documents/Perso/Environnments/influencer_networks/Scripts/activate

# Navigue dans le dossier du projet
cd ~/Documents/Perso/Portfolios/mapping-ytb-influencer-networks

# Exécute le script Python (test du shell)
# echo "Test !"
# python test.py

# Main pipeline
echo "Running main pipeline..."
python main.py

