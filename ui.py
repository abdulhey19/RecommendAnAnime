from tkinter import *
from tkinter import messagebox as mbx
from Anime import *
from PIL import ImageTk,Image
from translate import *

class Ui(Frame):
    def __init__(self):
        self.categories=getGenres()
        self.categories_url=getUrl()
        self.control=False
        self.colors={
            "labels":["#948979","#121481","#5BBCFF"],
            "fgcolors":["#0C0C0C","#222831","#240A34"],
            "buttons" :["#5F5D9C","#387ADF","#D04848"],
            "inputs":["#E9F6FF","#F8FAE5","#EEF5FF"]
        }
        self.ui()

    def ui(self):
        # screen
        window = Tk()
        window.configure(bg="#FFF")
        window.title("Recommend an Anime ")

        # pencereyi ekranın ortasında açmak için
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = 692
        window_height = 480
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")



        # labels
        lblgenres = Label(window, text="Genres", bd=0.9, bg=self.colors.get("labels")[2], fg="black", relief="solid")
        lblgenres.place(x=15.0, y=10.0, width=70.0, height=30.0)

        lbl_name = Label(window, text="Name", bd=0.9, bg=self.colors.get("labels")[2], fg="black", relief="solid")
        lbl_name.place(x=15.0, y=60.0, width=70.0, height=30.0)

        lbl_rank = Label(window, text="Rank", bd=0.9, bg=self.colors.get("labels")[2], fg="black", relief="solid")
        lbl_rank.place(x=15.0, y=110.0, width=70.0, height=30.0)

        lbl_categories = Label(window, text="Categories", bd=0.9, bg=self.colors.get("labels")[2], fg="black", relief="solid")
        lbl_categories.place(x=175.0, y=110.0, width=70.0, height=30.0)

        lbl_date = Label(window, text="Date", bd=0.9, bg=self.colors.get("labels")[2], fg="black", relief="solid")
        lbl_date.place(x=15.0, y=160.0, width=70.0, height=30.0)

        img = Image.open("anime.png")
        img = img.resize((200, 200))
        photo = ImageTk.PhotoImage(img)
        canvas=Canvas()
        canvas.place(x=470.0, y=10.0, width=210.0, height=210.0)
        canvas_no=canvas.create_image(105, 105, image=photo, tag="image_tag")

        # entries
        anime_name = Entry(window, bd=0, bg=self.colors.get("inputs")[2], fg="#000716", highlightthickness=0, state="disabled")
        anime_name.place(x=90.0, y=60.0, width=370.0, height=30.0)

        anime_date = Entry(window, bd=0,bg=self.colors.get("inputs")[2], fg="#000716", highlightthickness=0,state="disabled")
        anime_date.place(x=90.0, y=160.0, width=150.0, height=30.0)

        anime_rank = Entry(window, bd=0, bg=self.colors.get("inputs")[2], fg="#000716", highlightthickness=0, state="disabled")
        anime_rank.place(x=90.0, y=110.0, width=75.0, height=30.0)

        # textboxes
        anime_category = Text(window, bd=0, bg=self.colors.get("inputs")[1], fg="#000716", highlightthickness=0, state="disabled", padx=10,pady=10)
        anime_category.place(x=255.0, y=110.0, width=205.0, height=100.0)

        anime_desc = Text(window, bd=0, bg=self.colors.get("inputs")[1], fg="#000716", highlightthickness=0, state="disabled", padx=10, pady=10)
        anime_desc.place(x=15.0, y=230.0, width=662.0, height=240.0)


        # option menu
        OPTIONS =self.categories
        first_value = StringVar()
        first_value.set("Seçiniz...")
        oMenu = OptionMenu(window,first_value, *OPTIONS)
        oMenu.config(bg="#3652AD", fg="black",direction="right",indicatoron=False)
        oMenu.place(x=90.0, y=10.0, width=160.0, height=30.0)

        # buttons
        btnEnter = Button(window, text="Enter",borderwidth=0, highlightthickness=0, relief="flat", bg=self.colors.get("buttons")[1],
                          command=lambda: self.getRandomAnime(first_value,[anime_name,anime_date,anime_rank,anime_category,anime_desc,canvas],canvas_no))
        btnEnter.place(x=265.0, y=10.0, width=90.0, height=30.0)

        btnTranslate = Button(window, text="Translate",borderwidth=0, highlightthickness=0,relief="flat", bg=self.colors.get("buttons")[2],
                              command=lambda: self.translateText(anime_desc))
        btnTranslate.place(x=370.0, y=10.0, width=90.0, height=30.0)


        window.resizable(False, False)
        window.mainloop()

    def getRandomAnime(self, cmbbx, liste,sayi):
            self.control=False
            category=cmbbx.get()
            if category=="Seçiniz...":
                mbx.showerror("Warning", "Please Select Category")
            else:
                url = self.categories_url[self.categories.index(category)]
                infos = getAnimeName(url)
                cmbbx.set("Seçiniz...")
                self.openCloseState(liste, infos,sayi)

    def openCloseState(self, liste, infos,sayi):
        i = 0
        for info in infos:
            if isinstance(liste[i], Entry):
                liste[i].configure(state="normal")
                liste[i].insert("0", info)
                liste[i].configure(state="readonly")
            elif isinstance(liste[i], Text):
                liste[i].configure(state="normal")
                liste[i].insert(END, info)
                liste[i].configure(state="disabled")
            else:
                img = getImg(info)
                img = img.resize((200, 200))
                photo = ImageTk.PhotoImage(img)
                liste[i].itemconfig(sayi,image=photo)
                liste[i].image=photo
            i += 1

    def translateText(self,textArea):
        metin=translator.translate(textArea.get("0.0", END))
        if not self.control:
            if len(metin)!=0 and self.control==False:
                self.control=True
                textArea.configure(state="normal")
                textArea.delete("0.0", END)
                textArea.insert(END, metin)
                textArea.configure(state="disabled")

            else:
                mbx.showerror("Warning", "Metin Yok...")
        else:
            mbx.showerror("Warning", "Zaten Çevrilmiş...")

user=Ui()