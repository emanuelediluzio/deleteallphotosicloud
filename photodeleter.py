from pyicloud import PyiCloudService
from tqdm import tqdm

try:
    print("Inizio script...")
    # Autenticazione
    api = PyiCloudService('email', 'password')
    print("Autenticato.")

    # Verifica a due fattori se necessario
    if api.requires_2fa:
        print("Richiesta autenticazione a due fattori.")
        code = input("Inserisci il codice di verifica: ")
        result = api.validate_2fa_code(code)
        print("Codice verificato" if result else "Codice non valido")
    else:
        print("2FA non richiesto.")

    # Prova ad accedere alle foto
    try:
        # Se `all` è un attributo, non dovresti chiamarlo come una funzione.
        photos = api.photos.all
        # Potrebbe essere necessario convertire in lista se non è già un iterabile.
        photos_list = list(photos)
        print(f"Numero di foto da elaborare: {len(photos_list)}")
    except Exception as e:
        print(f"Errore nell'accesso alle foto: {e}")
        photos_list = []

    # Se ci sono foto, procedi con l'eliminazione
    if photos_list:
        # Definisci la funzione di eliminazione a blocchi
        def delete_photos_in_batches(photos, batch_size=500):
            for i in tqdm(range(0, len(photos), batch_size), desc="Eliminazione foto"):
                batch = photos[i:i+batch_size]
                for photo in batch:
                    # Assicurati che `delete` sia il metodo corretto per eliminare le foto.
                    photo.delete()
        
        # Elimina tutte le foto a blocchi di 1000
        delete_photos_in_batches(photos_list)
        print("Tutte le foto sono state eliminate.")
    else:
        print("Nessuna foto da eliminare.")

except Exception as e:
    print(f"Errore generale: {e}")



