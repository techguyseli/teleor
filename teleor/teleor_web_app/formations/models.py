from django.db import models

class TypeFormation(models.Model):
    description = models.CharField(max_length=60, unique=True)

class BrancheFormation(models.Model):
    description = models.CharField(max_length=60, unique=True)

class AttestationFormation(models.Model):
    description = models.CharField(max_length=60, unique=True)

class Formation(models.Model):
    initule_formation = models.CharField(max_length=60, unique=True)
    type_formation = models.ForeignKey('TypeFormation', on_delete=models.SET_NULL, null=True)
    branche_formation = models.ForeignKey('BrancheFormation', on_delete=models.SET_NULL, null=True)
    duree_formation_mois = models.PositiveIntegerField()
    duree_formation_heures = models.PositiveIntegerField()
    attestation_formation = models.ForeignKey('AttestationFormation', on_delete=models.SET_NULL, null=True)
    duree_stage = models.PositiveIntegerField()
    lien_cpf = models.URLField(null=True)
    tarif_sans_acompte = models.DecimalField(max_digits=7, decimal_places=2)
    acompte = models.DecimalField(max_digits=7, decimal_places=2)
    lien_brochure = models.URLField()
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(duree_formation_mois__gt=0) & models.Q(duree_formation_heures__gt=0), name='duree_formation_gte_0'),
            models.CheckConstraint(check=models.Q(tarif_sans_acompte__gt=0) & models.Q(acompte__gt=0), name='prix_gt_0')
                ]

class PrerequisScolaire(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

class PrerequisTechnique(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

class DureeEcheance(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    duree = models.PositiveIntegerField()
    class Meta:
        constraints = [
                models.CheckConstraint(check=models.Q(duree__gt=0), name='duree_gt_0'),
                ]

class Evolution(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

class Mission(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

class Avantage(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

class QualiteRequis(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)

class OrganismeEmploi(models.Model):
    formation = models.ForeignKey('Formation', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    

