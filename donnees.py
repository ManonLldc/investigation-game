# --- Suspects ---
suspects = {
    "Zyra": {
        "alibi": "Je passais la soirée dans la bibliothèque, entourée de vieux grimoires et de chandelles presque éteintes. J’avais l’impression de converser avec les esprits du manoir, comme souvent… mais je sais que personne ne m’a vraiment vue là-bas.",
        "indice": [
            "Une écharpe rouge accrochée au lustre du salon → quelqu’un est passé précipitamment par la pièce.",
            "Une plume de corbeau tombée sur le tapis de la bibliothèque → agitation dans la bibliothèque, preuve de présence de quelqu’un."
        ],
        "secret": "J’ai cru voir une ombre traverser le salon, rapide et silencieuse… J’ai détourné les yeux, pensant que c’était mon imagination, mais cette vision me hante encore.",
        "question_speciale": {
            "Que pensez-vous des esprits du manoir ?": "Ils murmurent parfois dans mon dos… Certains soirs, j’ai même l’impression qu’ils me suivent entre les pièces. Peut-être qu’ils savent plus que nous sur ce qui s’est passé.",
            "Que pensez-vous des autres suspects ?": "Nimue me rappelle les sorcières du passé, toujours à tripoter ses chaudrons… Elle cache plus qu’elle ne dit. Ophélia danse comme si la lune l’obsédait, je la trouve troublante. Grendel parle trop, ses histoires masquent peut-être quelque chose. Et Jean-Zeus… cet homme et son perroquet, je me demande parfois lequel des deux est le plus dérangé."
        }
    },
    "Nimue": {
        "alibi": "Je mélangeais des potions dans la cuisine, le chaudron a débordé plusieurs fois.",
        "indice": [
            "Une empreinte boueuse sur le rebord de la fenêtre → quelqu’un est passé dehors récemment.",
            "Un petit récipient d’herbes renversé sur le plan de travail → quelqu’un s’est déplacé précipitamment dans la cuisine."
        ],
        "secret": "Quelqu’un est passé près de moi en chuchotant, mais je n’ai pas pu distinguer qui.",
        "question_speciale": {
            "Quelle est votre potion préférée ?": "Une potion pour voir le passé… mais elle est instable et dangereuse.",
            "Que pensez-vous des autres suspects ?": "Zyra passe son temps à parler aux esprits, mais je crois surtout qu’elle fuit la réalité. Ophélia est belle quand elle danse, mais ses yeux… ils me font froid dans le dos. Grendel est sympathique, mais il cache sa nervosité derrière ses histoires. Jean-Zeus, lui, m’amuse, même si son perroquet répète parfois des mots qui me mettent mal à l’aise."
        }
    },
    "Ophelia": {
        "alibi": "Je faisais une danse étrange dans le jardin, appréciant la nuit et la lune.",
        "indice": [
            "Un bijou cassé trouvé près de la fontaine → quelqu’un a trébuché ou laissé tomber un objet près de la fontaine.",
            "Des traces humides autour de la fontaine → mouvement rapide ou fuite d’une personne."
        ],
        "secret": "Je me suis déplacée près de la fontaine, mais je n’ai rien vu de précis.",
        "question_speciale": {
            "Que faisiez-vous juste avant le crime ?": "Je marchais au bord de la fontaine, admirant le reflet de la lune…",
            "Que pensez-vous des autres suspects ?": "Zyra vit entourée de murmures invisibles, je ne sais pas si elle invente tout ça ou si elle entend vraiment quelque chose… Nimue prépare ses potions dans l’ombre, j’ai vu son regard changer quand je me suis approchée de la cuisine. Grendel rit trop fort pour être honnête, son vin et ses histoires ne m’inspirent pas confiance. Jean-Zeus ? Il m’observe souvent quand il pense que je ne le vois pas."
        }
    },
    "Grendel": {
        "alibi": "Je racontais des histoires de monstres aux invités dans le salon.",
        "indice": [
            "Une tache de vin sur le tapis du salon → chaos et agitation dans la pièce.",
            "Un papier froissé tombé sur la cheminée → quelqu’un a manipulé des documents en s’éloignant rapidement."
        ],
        "secret": "J’ai entendu un bruit suspect venant de l’étage, mais je n’y ai pas prêté attention.",
        "question_speciale": {
            "Quelle est la plus effrayante de vos histoires ?": "Celle d’un visiteur disparu dans le grenier, personne ne l’a jamais retrouvé…",
            "Que pensez-vous des autres suspects ?": "Zyra me glace avec ses histoires de fantômes. Elle regarde parfois dans le vide comme si elle voyait quelqu’un derrière moi… Nimue a l’air inoffensive, mais ses potions sentent parfois le poison. Ophélia danse dans le jardin comme une envoûtée… Qui sait ce qu’elle cache sous ses airs mystiques ? Jean-Zeus, enfin, fait rire son perroquet… mais j’ai surpris l’oiseau répéter une phrase inquiétante."
        }
    },
    "Jean-Zeus": {
        "alibi": "Je parlais à mon perroquet dans la bibliothèque pour lui enseigner des mots nouveaux.",
        "indice": [
            "Une porte du grenier entrouverte → passage récent d’un suspect dans le grenier.",
            "Quelques plumes multicolores éparpillées sur le sol → agitation dans la bibliothèque, preuve de déplacement rapide."
        ],
        "secret": "J’ai remarqué que certaines portes étaient entrouvertes, mais je n’ai rien touché.",
        "question_speciale": {
            "Que dit votre perroquet de la soirée ?": "Il répète parfois des mots étranges que je n’ai jamais prononcés…",
            "Que pensez-vous des autres suspects ?": "Zyra parle aux morts, moi je parle à mon perroquet. La différence ? Mon oiseau répond vraiment. Nimue bricole des mixtures étranges, je ne lui ferais pas goûter mon vin. Ophélia… elle a une façon de me regarder, comme si elle savait déjà quelque chose sur moi. Grendel, lui, a toujours un verre à la main, mais ses histoires me semblent parfois trop proches de la réalité."
        }
    }
}

# --- Coupable ---
COUPABLE = "Ophélia"

# --- Enquête (étapes du jeu) ---
enquete = {
    "debut": {
        "texte": (
            "🌙 Vous êtes détective, appelé d’urgence dans un manoir ancien et isolé.\n"
            "Un cri a déchiré la nuit, et un meurtre vient d’être commis dans l’ombre des couloirs silencieux.\n\n"
            "Les portes ont été verrouillées. Cinq personnes sont présentes dans la demeure, "
            "et l’une d’elles est le coupable… mais laquelle ?\n\n"
            "Votre mission : interroger les suspects, analyser leurs comportements, "
            "et rassembler les indices pour lever le voile sur la vérité."
        ),
        "choix": {
            "Interroger un suspect": "dossier_suspects",
            "Accuser quelqu'un": "accuser"
        }
    },
    "dossier_suspects": {
        "texte": "Voici la liste des suspects. Qui voulez-vous interroger ?",
        "choix": {}  # sera rempli automatiquement dans le jeu
    },
    "accuser": {
        "texte": "Qui accusez-vous ?",
        "choix": {}  # sera rempli automatiquement dans le jeu
    },
    "choisir_suspect": {
        "texte": "Choisissez un suspect à interroger.",
        "choix": {}  # sera rempli automatiquement
    }
}
