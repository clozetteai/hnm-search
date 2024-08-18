# Clozette.Ai

![](./assets/banner.png)

**Clozette.AI** we speak SQL, so you can speak fashion 😝. We translate your clothing descriptions into database queries, making it easier than ever to find the perfect outfit.

### Creators

- [Siddhant Prateek Mahanayak](https://github.com/siddhantprateek)
- [Anindyadeep](https://github.com/Anindyadeep)
- [Pratyush Patnaik](https://github.com/Pratyush-exe)


### Setting up the backend

To set up the backend you need to first create an environment
and install the requirements file. 

```
cd backend
pip install -r requirements.txt
```

Download all the assets from this [google drive link](https://drive.google.com/file/d/1OW_y8LNPishXXNOetkHR3ATC6rCm8R1u/view?usp=sharing) and place them in the `backend/assets` folder. After this paste this inside the `backend/assets` folder. Now unzip it inside the folder and you can delete the zip file.



For a sanity check, you can run the following command to see if the server is running.

```
# in the ./backend directory run:
uvicorn main:app --reload --port 7600

# And then test the runs by running the following command:

cd tests
pytest test_backend.py
```
