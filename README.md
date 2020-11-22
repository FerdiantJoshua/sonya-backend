# sonya-backend
Backend part of Sonya Chatbot for Kata.Ai Hackathon November 2020

## How to Run

1. Initialize project
    ```shell script
    make init
    ```

2. Put the model in `models/`

3. Run onmt_server  (you can customize the configuration in `app/onmt_server_conf.json`)
    ```shell script
    make run_onmt_server
    ```
   
4. In another procress, run API  (you can customize the configuration in `.env`)
    ```shell script
    make run_api_dev
    ```
   or
    ```shell script
    make run_api_prod
    ```
   
## How to Invoke API

Here is an example of invoking the API using Wget (replace the http://justquarter.changeip.co:30000/ with http://localhost:30000/ to invoke your locally-hosted endpoint):

```shell script
wget --quiet \
  --method POST \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: ' \
  --body-data '{"text": "Beyoncé Giselle Knowles-Carter (/ biːˈjɒnseɪ / bee-YON-say) (lahir 4 September 1981) adalah penyanyi, penulis lagu, produser dan aktris rekaman Amerika. Dilahirkan dan dibesarkan di Houston, Texas, ia tampil di berbagai kompetisi menyanyi dan menari sebagai seorang anak, dan mulai terkenal pada akhir 1990-an sebagai penyanyi utama grup gadis R&B Destiny'\''s Child. Dikelola oleh ayahnya, Mathew Knowles, kelompok ini menjadi salah satu kelompok gadis terlaris di dunia sepanjang masa. Hiatus mereka melihat rilis album debut Beyoncé, Dangerously in Love (2003), yang menetapkan dia sebagai artis solo di seluruh dunia, memperoleh lima Grammy Awards dan menampilkan Billboard Hot 100 nomor satu single \"Crazy in Love\" dan \"Baby Boy\"".","n_questions": "max"}' \
  --output-document \
  - http://justquarter.changeip.co:30000/
```

## Authors

Tim Athena
